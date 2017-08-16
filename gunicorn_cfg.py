import multiprocessing
# http://docs.gunicorn.org/en/stable/settings.html
workers = multiprocessing.cpu_count() * 2 + 1
# defult port:
bind = '127.0.0.1:5000'
keepalive = 2
timeout = 30  # worker
# supervisorctl catch logs (log_rider_access.log):
accesslog = '-'
errorlog = '-'
