#!/usr/bin/env bash

# Visibilidad para gunicorn
export APP_BIND=$APP_BIND

# TODO: rename virtualenv with your env:
exec /home/ubuntu/.virtualenvs/tpl_project/bin/gunicorn app:app -c gunicorn_cfg.py
