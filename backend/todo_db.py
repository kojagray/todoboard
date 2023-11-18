import sqlite3
from todoist_api_wrapper import TodoistAPIWrapper

DB_FP = "./todo.db"

def create_connection():
    try:
        connection = sqlite3.connect(DB_FP)
        return connection
    except Error as e:
        print(e)


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


if __name__ == "__main__":
    update_tasks()




    