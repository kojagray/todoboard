import requests
from tinydb import TinyDB, Query
import tqdm

from todoist_api_python.api import TodoistAPI

class TodoDB:
    def __init__(self):
        self.db = TinyDB("data/todo_db.json")

class Todoist:
    def __init__(self):
        self.api_key = self._get_api_key()
        self.api = self._init_api()

    def _get_api_key(self):
        with open("data/apikey.txt", "r") as rp:
            api_key = rp.read()
            
            return api_key

    def _init_api(self):
        api = TodoistAPI(self.api_key)
        
        return api 
        
    def get_all_projects(self):
            try:
                projects = self.api.get_projects()
                return projects
            except Exception as error:
                print(error)

    def get_completed_tasks(self, num_tasks=200):
        get_all_url = 'https://api.todoist.com/sync/v9/completed/get_all'
        headers = {'Authorization': 'Bearer {}'.format(self.api_key)}
        params = {
            "limit": num_tasks,
            "annotate_notes": "true"
        }

        try:
            response = requests.get(
                            get_all_url, 
                            headers=headers,
                            params=params)  
            return response.json()
            
        except Exception as error:
            print(error) 

    def get_task_details(self, task_id):
        task_details_url = 'https://api.todoist.com/sync/v9/items/get'
        headers = {'Authorization': 'Bearer {}'.format(self.api_key)}
        data = {'item_id': task_id}

        try:
            response = requests.post(task_details_url, headers=headers, data=data)
            return response
        except Exception as error:
            print(error)

    def update_tasks(self):
        pass 