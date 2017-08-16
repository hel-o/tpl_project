from datetime import timedelta

import redis as _redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase
from flask_session import Session


class RedisExt(_redis.Redis):

    def init_app(self, my_app):
        self.__init__(host=my_app.config['REDIS_HOST'])


redis = RedisExt()


class SQLAlchemy(SQLAlchemyBase):
    """Postgres use PgBouncer:"""

    def apply_driver_hacks(self, app, info, options):
        super(SQLAlchemy, self).apply_driver_hacks(app, info, options)
        from sqlalchemy.pool import NullPool
        options['poolclass'] = NullPool
        options.pop('pool_size', None)
        options.pop('max_overflow', None)

db = SQLAlchemy()


def create_app():
    import config
    my_app = Flask(__name__)
    my_app.config.from_object(config)

    db.init_app(my_app)

    redis.init_app(my_app)
    # config for Session:
    my_app.permanent_session_lifetime = timedelta(days=1)
    my_app.config['SESSION_TYPE'] = 'redis'
    my_app.config['SESSION_REDIS'] = redis
    my_app.config['SESSION_USE_SIGNER'] = True
    my_app.config['SESSION_KEY_PREFIX'] = 'tpl-project'

    Session(my_app)

    from app.frontend.views import urls_frontend
    from app.api import api_resource1

    my_app.register_blueprint(urls_frontend)
    my_app.register_blueprint(api_resource1)

    return my_app


app = create_app()
