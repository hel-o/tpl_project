import random
import string

import redis as _redis
from flask import session, g
from flask_session import Session as FlaskSession, RedisSessionInterface
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase
from werkzeug.contrib.cache import RedisCache
from itsdangerous import JSONWebSignatureSerializer


migrate = Migrate()


class RedisCacheExt(object):
    _redis_cache = None

    def init_app(self, my_app):
        self._redis_cache = RedisCache(
            host=my_app.config['REDIS_HOST']
        )

    def set(self, key, value, timeout=None):
        self._redis_cache.set(key, value, timeout)

    def get(self, key):
        return self._redis_cache.get(key)


redis_cache = RedisCacheExt()


class RedisExt(_redis.Redis):

    def init_app(self, my_app):
        self.__init__(host=my_app.config['REDIS_HOST'])


redis = RedisExt()


class SQLAlchemy(SQLAlchemyBase):
    """Se usará PgBouncer, configurar NullPoll para que SQLAlchemy no maneje su propio Pool."""

    def apply_driver_hacks(self, app, info, options):
        super(SQLAlchemy, self).apply_driver_hacks(app, info, options)
        from sqlalchemy.pool import NullPool
        options['poolclass'] = NullPool
        options.pop('pool_size', None)
        options.pop('max_overflow', None)


db = SQLAlchemy()


class JWSerializerEX(object):
    """Crea la instancia para el JWSSignature serializar, puede en otras versiones cambie el
    nombre del algoritmo por defecto (ya pasó 0.24 .. 1.1.0), es mejor espeficiar."""

    def __init__(self):
        self.jws: JSONWebSignatureSerializer = None

    def init_app(self, my_app):
        self.jws = JSONWebSignatureSerializer(my_app.config['SECRET_KEY'], algorithm_name='HS512')

    def loads(self, s):
        return self.jws.loads(s)

    def dumps(self, obj):
        return self.jws.dumps(obj)


jws_serializer = JWSerializerEX()


class RedisSessionHacked(RedisSessionInterface):
    """Clase customizada para evitar crear y mantener
    las key de las sesiones en redis en cada request cuando
    las Apis públicas son consumidas, en vez de eso el request
    envia el token de autorización."""

    def save_session(self, my_app, the_session, response):
        if g.get('no_session'):
            return

        super().save_session(my_app, the_session, response)


class SessionHacked(FlaskSession):
    """Clase customizada para asignar el redis de manera
    directa el redis como backed para las sesiones"""

    def init_app(self, my_app):
        config = my_app.config.copy()
        # my_app.session_interface = self._get_interface(my_app)
        my_app.session_interface = RedisSessionHacked(
            redis=config['SESSION_REDIS'],
            key_prefix=config['SESSION_KEY_PREFIX'],
            use_signer=config['SESSION_USE_SIGNER'],
            permanent=config['SESSION_PERMANENT']
        )


def generate_csrf_token():
    if 'csrf_token' not in session:
        csrf_token = ''.join([random.choice(string.ascii_letters + string.digits)
                              for i in range(32)])
        session['csrf_token'] = csrf_token
    return session['csrf_token']

