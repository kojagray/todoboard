from datetime import datetime, date, timedelta
from dateutil import parser, tz
import sqlite3

from todoist_api_wrapper import TodoistAPIWrapper

ISO8601_UTC_STRF = '%Y-%m-%dT%H:%M:%S.%fZ'
ISO8601_LOCAL_STRF = '%Y-%m-%dT%H:%M:%S.%f'
ISO_DATE_STRF = '%Y-%m-%d'

DB_FP = "./todo.db"


def last_weeks_tasks():
    connection = create_connection()
    cursor = connection.cursor()
    q = f"SELECT * from tasks WHERE strftime(\"{ISO8601_UTC_STRF}\", completed_at) > (SELECT DATETIME('now', '-7 day'))"
    cursor.execute(q)
    tasks = [sql_fetch_to_dict(task, cursor) for task in cursor.fetchall()]

    last_weeks_tasks = generate_last_week_map()
    for task in tasks:
        local_completed_time = utc_to_local(task['completed_at'])
        task['local_complete_time'] = local_completed_time
        date_completed = iso8601_datetime_string_to_date(local_completed_time)
        if date_completed in last_weeks_tasks:
            last_weeks_tasks[date_completed].append(task)

    return last_weeks_tasks


def update_tasks():
    print("Checking for new tasks...")
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * from tasks")
    current_tasks = cursor.fetchall()
    current_task_keys = {t[0] for t in current_tasks}

    T = TodoistAPIWrapper()
    new_tasks = T.get_completed_tasks()['items']
    
    task_ingest_cmds = []
    for task in new_tasks:
        if task['id'] not in current_task_keys:
            cmd = (
                task["id"], 
                task["content"], 
                task["project_id"], 
                task["section_id"], 
                task["completed_at"]
            )
            task_ingest_cmds.append(cmd)
    
    for task in task_ingest_cmds:
        print(f"Adding task: {str(task)}")

    cursor.executemany("INSERT into tasks values (?, ?, ?, ?, ?)", task_ingest_cmds)
    connection.commit()
    print(f"{len(task_ingest_cmds)} tasks added!")
    connection.close()


def get_project_info(task_id):
    connection = create_connection()
    cursor = connection.cursor()
    q = "SELECT * from tasks WHERE id = ?"
    cursor.execute(q, (task_id,))
    task = cursor.fetchone()
    project_id = task[2]

    q = "SELECT * from projects where id = ?"
    cursor.execute(q, (project_id,))
    project = cursor.fetchone()
    
    return project


def get_hex_from_color_name(color_name):
    connection = create_connection()
    cursor = connection.cursor()
    q = "SELECT hexadecimal from colors WHERE name = ?"
    cursor.execute(q, (color_name,))
    hexa = cursor.fetchone()
    
    return hexa[0]


def create_connection():
    try:
        connection = sqlite3.connect(DB_FP)
        return connection
    except Error as e:
        print(e)


def generate_last_week_map():
    today = date.today()
    last_week_map = {}
    for i in range(7):
        day = today - timedelta(days=i)
        iso = day.isoformat()
        last_week_map[iso] = []
    
    return last_week_map


def iso8601_datetime_string_to_date(dtstring):
    return dtstring.split("T")[0]


def sql_fetch_to_dict(qrow, cursor):
    '''
    Converts sql query tuples into dictionary with row headers as keys
    '''
    headers = [x[0] for x in cursor.description]
    
    qdict = {}
    for i, header in enumerate(headers):
        qdict[header] = qrow[i]

    return qdict


def utc_to_local(iso_utc_string):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = datetime.strptime(iso_utc_string, ISO8601_UTC_STRF)
    utc = utc.replace(tzinfo=from_zone)
    local_dt = utc.astimezone(to_zone)
    iso_local_string = local_dt.strftime(ISO8601_LOCAL_STRF)

    return iso_local_string