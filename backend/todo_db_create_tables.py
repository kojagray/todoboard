import pandas as pd 
import sqlite3 
from todoboard import Todoist

connection = sqlite3.connect("data/todo.db")
cursor = connection.cursor()

create_sections_table_cmd = "CREATE table sections ("
create_sections_table_cmd += "id text, "
create_sections_table_cmd += "project_id text, "
create_sections_table_cmd += "name text"
create_sections_table_cmd += ");"
cursor.execute(create_sections_table_cmd)
connection.commit()
print(f"Executing command: {create_sections_table_cmd}")

create_projects_table_cmd = "CREATE table projects ("
create_projects_table_cmd += "id text, "
create_projects_table_cmd += "name text, "
create_projects_table_cmd += "color text"
create_projects_table_cmd += ");"
cursor.execute(create_projects_table_cmd)
connection.commit()
print(f"Executing command: {create_projects_table_cmd}")

create_tasks_table_cmd = "CREATE table tasks ("
create_tasks_table_cmd += "id text, " 
create_tasks_table_cmd += "content text, "
create_tasks_table_cmd += "project_id text, "
create_tasks_table_cmd += "section_id text, "
create_tasks_table_cmd += "completed_at text" 
create_tasks_table_cmd += ");"
cursor.execute(create_tasks_table_cmd)
connection.commit()
print(f"Executing command: {create_tasks_table_cmd}")

create_colors_table_cmd = "CREATE table colors ("
create_colors_table_cmd += "id integer, "
create_colors_table_cmd += "name text, "
create_colors_table_cmd += "hexadecimal text"
create_colors_table_cmd += ");"
cursor.execute(create_colors_table_cmd)
connection.commit()
print(f"Executing command: {create_colors_table_cmd}")

# initialize Todoist API wrapper constructor 
T = Todoist()

# ingest projects 
projects = T.get_all_projects()
project_ingest_cmds = []
for project in projects:
    cmd = (project.id, project.name, project.color) 
    project_ingest_cmds.append(cmd)
cursor.executemany("INSERT into projects values (?, ?, ?)", project_ingest_cmds)
connection.commit()
print("Ingested projects!")

# ingest sections 
sections = T.get_sections()
section_ingest_cmds = []
for section in sections:
    cmd = (section.id, section.project_id, section.name) 
    section_ingest_cmds.append(cmd)
cursor.executemany("INSERT into sections values (?, ?, ?)", section_ingest_cmds)
connection.commit()
print("Ingested sections!")

# ingest colors
colors = pd.read_csv("data/colors.csv")
color_ingest_cmds = []
for _, color in colors.iterrows():
    cmd = (color['ID'], color['Name'], color['Hexadecimal'])
    color_ingest_cmds.append(cmd)
cursor.executemany("INSERT into colors values (?, ?, ?)", color_ingest_cmds)
connection.commit()
print("Ingested colors!")

# ingest tasks
tasks = T.get_completed_tasks()
task_ingest_cmds = []
for task in tasks['items']:
    section_id = ""
    cmd = (
        task["id"], 
        task["content"], 
        task["project_id"], 
        task["section_id"], 
        task["completed_at"]
    )
    task_ingest_cmds.append(cmd)
cursor.executemany("INSERT into tasks values (?, ?, ?, ?, ?)", task_ingest_cmds)
connection.commit()
print("Ingested tasks!")

connection.close()
