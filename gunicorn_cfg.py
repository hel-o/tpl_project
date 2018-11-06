import os
import multiprocessing

# http://docs.gunicorn.org/en/stable/settings.html
workers = multiprocessing.cpu_count() * 2 + 1
bind = os.environ.get('APP_BIND', '127.0.0.1:5000')
keepalive = 2
timeout = 5
accesslog = '-'  # supervisorctl catch logs
errorlog = '-'
access_log_format = '%({X-Forwarded-For}i)s %(p)s %(L)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
