#!/usr/bin/env bash

# TODO: use your own var env:
export TPL_PROJECT_PRODUCTION=1

# TODO: rename virtualenv with your env:
exec /home/ubuntu/.virtualenvs/tpl_project/bin/gunicorn app:app -c gunicorn_cfg.py
