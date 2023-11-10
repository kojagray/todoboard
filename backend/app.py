from datetime import datetime, date, timedelta
from dateutil import parser
import pickle

from todoboard import TodoDB, Todoist

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

#TODO: This is obviously very time-consuming. We need to have some kind of database.
# todoist = Todoist()
# completed = todoist.get_completed_tasks()

# this will do for now...
with open("./data/tasks.p", "rb") as rp:
    task_data = pickle.load(rp)


@app.route("/most_recent")
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def return_most_recent_task():
    return jsonify(task_data['items'][0])


@app.route("/last_week")
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def return_last_weeks_tasks():
    task_items = task_data['items']
    payload = {"last_weeks_tasks": []}
    for task in task_items:
        if from_last_week(task):
            dt = iso8601_to_datetime(task['completed_at'])
            weekday = weekday_from_datetime(dt)
            date = dt.date()
            payload['last_weeks_tasks'].append(
                {
                    "date" : date,
                    "weekday" : weekday,
                    "task_content" : task['content']
                }
            )

    return jsonify(payload)


def from_last_week(task):
    completed_at = iso8601_to_datetime(task['completed_at'])
    last_week = (
        datetime.now() - timedelta(days=7)
    ).date()
    last_week = datetime.combine(last_week, datetime.min.time())
    if completed_at > last_week:
        return True
    return False


def weekday_from_datetime(dt):
    weekday_map = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]
    return weekday_map[dt.weekday()]


def iso8601_to_datetime(isodatetime):
    #TODO: Making the datetime tz-naive might be a problem later...?
    return parser.parse(isodatetime).replace(tzinfo=None)
