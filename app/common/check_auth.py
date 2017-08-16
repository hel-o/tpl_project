from functools import wraps

from flask import (request, abort, current_app, g, session, redirect, url_for)
from itsdangerous import (JSONWebSignatureSerializer as Serializer,
                          BadSignature)

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
            serializer = Serializer(current_app.config['SECRET_KEY'])
            try:
                g.token_values = serializer.loads(request.headers['Authorization'])
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
