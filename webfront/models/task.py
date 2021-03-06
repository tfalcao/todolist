__author__ = 'cody'

from webfront.models import LocalBase
from utils.rest_api_utils import *
from datetime import datetime, timedelta

class LocalTask(LocalBase):
    pass

class TaskManager(RestClient):

    def __init__(self, api_url):
        super().__init__(api_url)

    def get_task(self, task_id):
        response_obj, status = self.get_resource("task/{}".format(task_id))
        if status != HTTPStatusCodes.OK:
            print(response_obj)
            return None
        return LocalTask(response_obj["data"])

    def get_all_tasks(self):
        response_obj, status = self.get_resource("task")
        if status != HTTPStatusCodes.OK:
            print(response_obj)
            return None
        return [LocalTask(data) for data in response_obj["data"]]

    def save_new_task(self, local_task):
        response_obj, status = self.post_resource("task", data=local_task.copy())
        if status != HTTPStatusCodes.CREATED:
            print(response_obj)
        return response_obj

    def update_existing_task(self, local_task):
        response_obj, status = self.put_resource("/task/{}".format(local_task["id"]), data=local_task.copy())
        if status != HTTPStatusCodes.OK:
            print(response_obj)
        return response_obj

    def delete_task(self, task_id):
        response_obj, status = self.delete_resource("/task/{}".format(task_id))
        if status != HTTPStatusCodes.NO_CONTENT:
            print(response_obj)
        return response_obj

    def finish_task(self, task_id):
        response_obj, status = self.post_resource("/task/{}/finish".format(task_id))
        if status != HTTPStatusCodes.OK:
            print(response_obj)
        return response_obj



