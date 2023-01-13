import requests

from todoist_api_python.api import TodoistAPI

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
            completed_tasks = response.json()['items']
            return completed_tasks
        except Exception as error:
            print(error) 
            pass 