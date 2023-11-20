from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from todo_db import (
    last_weeks_tasks, 
    update_tasks
)

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/last_weeks_tasks")
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def last_weeks_tasks_endpoint():
    tasks = last_weeks_tasks()

    return jsonify(tasks)


if __name__ == "__main__":
    update_tasks()
    app.run(debug=True, port=8080)
