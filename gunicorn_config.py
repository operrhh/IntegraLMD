import gevent.monkey
gevent.monkey.patch_all()

bind = "0.0.0.0:8080"
workers = 12
worker_class = "gevent"
timeout = 300
