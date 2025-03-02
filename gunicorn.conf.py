import multiprocessing
import os
from pathlib import Path

# Use project-level logs directory
current_dir = Path(__file__).parent
LOG_DIR = current_dir / 'logs'

# Create logs directory if needed
LOG_DIR.mkdir(exist_ok=True)

# Use port 8000 instead of 80
bind = ['0.0.0.0:8000']
workers = multiprocessing.cpu_count() * 2 + 1

accesslog = str(LOG_DIR / 'access.log')
errorlog = str(LOG_DIR / 'error.log')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
capture_output = True
