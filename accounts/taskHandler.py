from enum import Enum
from django.core.cache import cache
import threading
from typing import Union
from uuid import uuid1

class TaskHandler:

    def start_task(self, method, args):

        task_progress = TaskProgress()
        t = threading.Thread( target=method, args=[ *args, task_progress ] )
        t.setDaemon(True)
        t.start()

        return task_progress.get_task_id()

    @staticmethod
    def get_task_progress( task_id : str ):
        return cache.get( task_id )

class TaskProgress:

    task_id = str

    # default constructor
    def __init__(self):
        self.task_id = str( uuid1() )
        cache.set( self.task_id, self, 3600 )

    def set( self,
        status : Enum,
        progress_message : Union[ str, None ] = None,
        output : Union[ str, None ] = None,) -> object:

        self.status = status.value
        self.progress_message = progress_message
        self.output = output

        cache.set( self.task_id, self, 3600 )

    def get_task_id( self ):
        return self.task_id

class Status(Enum):
    STARTED = 'STARTED'
    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'

# code from: https://ivanyu2021.hashnode.dev/a-simple-approach-for-background-task-in-django <3