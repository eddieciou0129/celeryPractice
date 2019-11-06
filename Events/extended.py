from datetime import datetime
from celery.backends.mongodb import MongoBackend
from celery import Celery
from celery.result import AsyncResult
from celery._state import get_current_task
from celery.utils.log import ColorFormatter
from celery.exceptions import ImproperlyConfigured
from kombu.utils.encoding import bytes_to_str
from kombu.utils.objects import cached_property


class TaskFormatter(ColorFormatter):
    """
    Formatter for tasks, adding the task name and id.
    Customize Log Formatter add root_id
    """
    def format(self, record):
        self.use_color = False
        task = get_current_task()
        if task and task.request:
            record.__dict__.update(
                root_id=task.request.root_id,
                task_id=task.request.id,
                task_name=task.name)
        else:
            record.__dict__.setdefault('task_name', None)
            record.__dict__.setdefault('task_id', None)
            record.__dict__.setdefault('root_id', None)
        return ColorFormatter.format(self, record)


class ExtendedCelery(Celery):
    @cached_property
    def AsyncResult(self):
        """
        Override the default result class of Celery
        """
        return self.subclass_with_self(ExtendedAsyncResult)


class ExtendedMongoBackend(MongoBackend):
    def _get_database(self):
        #  複寫DB 不然預設都只能存 admin
        conn = self._get_connection()
        db = conn[self.database_name]
        custom_db = conn["event"]
        if self.user and self.password:
            if not db.authenticate(self.user, self.password):
                raise ImproperlyConfigured('Invalid MongoDB username or password.')
        return custom_db

    def _store_result(self, task_id, result, state, traceback=None, request=None, **kwargs):
        # 複寫 result backend 儲存資訊
        meta = {
            # '_id': task_id,
            'status': state,
            'result': self.encode(result),
            'date_done': datetime.utcnow(),
            'traceback': self.encode(traceback),
            'children': self.current_task_children(request),
            'task_id': bytes_to_str(task_id),
            'root_id': bytes_to_str(request.root_id),
            'parent_id': bytes_to_str(request.parent_id),
            'name': request.task,
            'args': request.args,
            'kwargs': request.kwargs,
            'worker': request.hostname,
            'retries': request.retries,
            'queue': request.delivery_info['routing_key']
        }
        self.collection.save(meta)
        return result


class ExtendedAsyncResult(AsyncResult):
    @property
    def name(self):
        return self._get_task_meta().get('name')

    @property
    def args(self):
        return self._get_task_meta().get('args')

    @property
    def kwargs(self):
        return self._get_task_meta().get('kwargs')

    @property
    def worker(self):
        return self._get_task_meta().get('worker')

    @property
    def date_done(self):
        return self._get_task_meta().get('date_done')

    @property
    def retries(self):
        return self._get_task_meta().get('retries')

    @property
    def queue(self):
        return self._get_task_meta().get('queue')
