# myproject/celery.py
import os
from celery import Celery

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

# Auto-discover tasks in installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')