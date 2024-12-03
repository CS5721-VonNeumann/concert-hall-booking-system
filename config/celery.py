from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, Task
from celery import bootsteps
from kombu import Exchange, Queue
from celery.exceptions import Reject, MaxRetriesExceededError

import environ

# Initialize environment reading
env = environ.Env()

# Load environment file if it exists
env_name = os.getenv('ENV', 'development')
env_file = f".env.{env_name}"
if os.path.exists(env_file):
    environ.Env.read_env(env_file)
    print(f"Loading environment from {env_file}")
else:
    print(f"Warning: {env_file} not found. Using default settings.")
    
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')


default_queue_name = 'default'
default_exchange_name = 'default'
default_routing_key = 'default'
deadletter_suffix = 'deadletter'
deadletter_queue_name = default_queue_name + f'.{deadletter_suffix}'
deadletter_exchange_name = default_exchange_name + f'.{deadletter_suffix}'
deadletter_routing_key = default_routing_key + f'.{deadletter_suffix}'


class DeclareDLXnDLQ(bootsteps.StartStopStep):
    """
    Celery Bootstep to declare the DL exchange and queues before the worker starts
        processing tasks
    """
    requires = {'celery.worker.components:Pool'}

    def start(self, worker):
        app = worker.app

        # Declare DLX and DLQ
        dlx = Exchange(deadletter_exchange_name, type='direct')

        dead_letter_queue = Queue(
            deadletter_queue_name, dlx, routing_key=deadletter_routing_key)

        with worker.app.pool.acquire() as conn:
            dead_letter_queue.bind(conn).declare()



default_exchange = Exchange(default_exchange_name, type='direct')
default_queue = Queue(
    default_queue_name,
    default_exchange,
    routing_key=default_routing_key,
    queue_arguments={
        'x-dead-letter-exchange': deadletter_exchange_name,
        'x-dead-letter-routing-key': deadletter_routing_key
    })

app.conf.task_queues = (default_queue, )

# Add steps to workers that declare DLX and DLQ if they don't exist
app.steps['worker'].add(DeclareDLXnDLQ)

app.conf.task_default_queue = default_queue_name
app.conf.task_default_exchange = default_exchange_name
app.conf.task_default_routing_key = default_routing_key

# Auto-discover tasks in installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)  # Exceptions to retry on
    retry_kwargs = {'max_retries': 3}
    retry_backoff = True  # Enables exponential backoff
    retry_backoff_max = 60  # Maximum backoff in seconds
    retry_jitter = True  # Adds randomness to prevent stampedes

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        Handle task failure. If max retries exceeded, reject the task.
        """
        print(f"Task {self.name} exceeded max retries. Rejecting...")
        # Reject the task to send it to DLQ
        raise Reject(requeue=False)