from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from todo_db import (
    last_weeks_tasks, 
    update_tasks,
    get_all_tasks,
    get_all_projects,
    get_project_info,
    get_hex_from_color_name,
    generate_all_tasks_counter
)

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/per_project_date_counter")
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def per_project_date_counter_endpoint():
    projects = get_all_projects()
    project_map = {p['id'] : [] for p in projects}
    tasks = get_all_tasks()
    for task in tasks:
        pid = task['project_id']
        project_map[task['project_id']].append(task)

    project_map = {
        pid : {
            "project_name" : get_project_info(pid)['name'],
            'project_color' : get_hex_from_color_name(get_project_info(pid)['color']),
            "counter" : generate_all_tasks_counter(tasks)
        }
        for pid, tasks in project_map.items()
        if get_project_info(pid)['name'] != "Inbox"
    }
    return jsonify(project_map)


@app.route("/all_tasks_date_counter")
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def all_tasks_date_counter_endpoint():
    tasks = get_all_tasks()
    tasks_counter = generate_all_tasks_counter(tasks)

    return jsonify(tasks_counter)

@app.route("/all_tasks")
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def all_tasks_endpoint():
    tasks = get_all_tasks()

    return jsonify({"all_tasks" : tasks})


@app.route("/last_weeks_tasks")
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def last_weeks_tasks_endpoint():
    tasks = last_weeks_tasks()

    return jsonify(tasks)


@app.route("/update_tasks")
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def update_tasks_endpoint():
    update_tasks()

    return '', 204


if __name__ == "__main__":
    update_tasks()
    app.run(debug=True, port=8080)
