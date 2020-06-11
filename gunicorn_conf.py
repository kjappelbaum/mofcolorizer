# -*- coding: utf-8 -*-
# pylint:disable=invalid-name
"""Settings for gunicorn"""

#https://pythonspeed.com/articles/gunicorn-in-docker/
worker_tmp_dir = '/dev/shm'
workers = 2
threads = 4
worker_class = 'gthread'
