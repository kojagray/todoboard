from datetime import datetime, timezone
from dateutil import parser 
import requests

from tinydb import TinyDB, Query
from todoist_api_python.api import TodoistAPI

class TodoDB:
    def __init__(self):
        self.api_key = self._get_api_key()
        self.api = self._init_api()
        self.db = TinyDB("data/todo_db.json")

    def update_db(self):
        '''
        Gets timestamp of most recent task,
        Then performs a get_completed_tasks() with "since" parameter
        Then ingests tasks into database
        '''
        ct_table = self.db.table("completed_tasks")
        if ct_table.all():
            most_recent = ct_table[0]
            timestamp = most_recent['timestamp'].split(".")[0]
            new_ct_data = self.api.get_completed_tasks(since=timestamp)
        else:
            new_ct_data = self.api.get_completed_tasks()
        ct_table.insert_multiple(new_ct_data)


    def get_all_projects(self):
            try:
                projects = self.api.get_projects()
                return projects
            except Exception as error:
                print(error)


    def get_completed_tasks(self, since=None):
        get_all_url = 'https://api.todoist.com/sync/v9/completed/get_all'
        headers = {'Authorization': 'Bearer {}'.format(self.api_key)}
        
        params = {
            "annotate_notes": "true",
            "limit": 200
        }
        if since:
            params["since"] = since

        try:
            response = requests.get(
                            get_all_url, 
                            headers=headers,
                            params=params)  
            cts = response.json()['items']
            # add local timestamp
            completed_tasks = []
            for ct in cts:
                ct['completed_at_lt'] = self._utc_to_local(ct['completed_at'])
                ct['completed_at_utc'] = ct["completed_at"]
                del ct["completed_at"]
                completed_tasks.append(ct)
            return completed_tasks
        except Exception as error:
            print(error) 
            pass 

    def _get_api_key(self):
        with open("data/apikey.txt", "r") as rp:
            api_key = rp.read()
            
            return api_key

    def _init_api(self):
        api = TodoistAPI(self.api_key)
        
        return api 

    def _utc_to_local(self, utc_str):
        utc_dt = parser.parse(utc_str)
        local_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
        local_str = local_dt.strftime("%Y-%m-%dT%H:%M:%S")

        return local_str    