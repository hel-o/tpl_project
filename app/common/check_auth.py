from functools import wraps

from itsdangerous import BadSignature
from flask import request, abort, g, session, redirect, url_for

from app.extensions import jws_serializer
from app.common.constants import TipoUsuario


def check_api_auth(f):
    """
    check auth for api
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers.keys():
            abort(401)
        else:
            try:
                g.token_values = jws_serializer.loads(request.headers['Authorization'])
            except BadSignature:
                abort(401)
        return f(*args, **kwargs)
    return wrapper


def requires_auth(user_type, url_redirect=True):
    """
    check auth for views, internal use:
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # check if user are login:
            if not session.get('nombre', None):
                if url_redirect:
                    return redirect(url_for('urls_common.login'))
                else:  # unauthorized:
                    return abort(401)
            # else check if has the permission, using bitwise operator:
            if not (session['tipo'] & user_type == session['tipo']):
                if session['tipo'] == TipoUsuario.ADMIN:
                    return redirect(url_for('urls_admin.home'))
                return abort(403)

            return f(*args, **kwargs)
        return wrapped
    return wrapper


def csrf_protect(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if request.method == 'POST':
            csrf_token = session.pop('csrf_token', None)
            if not csrf_token or not csrf_token == request.form.get('csrf_token', None):
                abort(403)
        return f(*args, **kwargs)
    return wrapped
