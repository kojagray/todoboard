from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from todo_db import (
    last_weeks_tasks, 
    update_tasks,
    get_all_tasks,
    generate_all_tasks_counter
)

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route("/all_tasks_date_counter")
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def all_tasks_date_counter_endpoint():
    tasks = get_all_tasks()
    tasks_counter = generate_all_tasks_counter(tasks)
    print(tasks_counter)

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
