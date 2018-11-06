import os
from datetime import timedelta

from flask import Flask

import config
from .extensions import db, migrate, redis, redis_cache, jws_serializer, SessionHacked, generate_csrf_token


def create_app(app_name='web'):
    my_app = Flask(__name__)
    my_app.config.from_object(config)

    if os.environ.get('APP_CONFIG'):
        my_app.config.from_pyfile(os.environ.get('APP_CONFIG'))

    # extensions:
    db.init_app(my_app)
    migrate.init_app(my_app)

    if app_name == 'web':
        # web extensions:
        redis.init_app(my_app)
        redis_cache.init_app(my_app)
        jws_serializer.init_app(my_app)

        # Config session:
        my_app.permanent_session_lifetime = timedelta(weeks=1)
        my_app.config['SESSION_TYPE'] = 'redis'
        my_app.config['SESSION_REDIS'] = redis
        my_app.config['SESSION_USE_SIGNER'] = True
        my_app.config['SESSION_KEY_PREFIX'] = 'tpl_project'  # TODO: prefix.
        my_app.config['SESSION_PERMANENT'] = True  # default

        my_session = SessionHacked()
        my_session.init_app(my_app)

        my_app.jinja_env.globals['csrf_token'] = generate_csrf_token

        from app.frontend.views import urls_frontend
        from app.api.v1 import api_resource1

        my_app.register_blueprint(urls_frontend)
        # apis:
        url_prefix = '/api/v1'
        my_app.register_blueprint(api_resource1, url_prefix=url_prefix)

    return my_app


app = create_app()
