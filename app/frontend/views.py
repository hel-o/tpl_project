from flask import (Blueprint, render_template, session,
                   redirect, url_for, request)
from flask.views import MethodView

from app.common.models import Usuario
from app.common.check_auth import csrf_protect
from app.common.constants import TipoUsuario


urls_frontend = Blueprint(
    'urls_frontend',
    __name__
)


class LoginView(MethodView):

    decorators = [csrf_protect]
    template_name = 'login.html'

    def get(self, message=None):
        if session.get('nombre'):
            return redirect(url_for('.home'))
        return render_template(self.template_name, message=message)

    def post(self):
        usuario = Usuario.validar_usuario(request.form.get('username'),
                                          request.form.get('password'))
        if usuario:
            session['nombre'] = usuario.nombre
            session['tipo'] = usuario.tipo
            session['usuario_id'] = usuario.id

            if usuario.tipo == TipoUsuario.ADMIN:
                return redirect(url_for('.admin_home_view'))

            return redirect(url_for('.home'))
        return self.get(message=u'Usuario y/o contraseñas inválidos!')


urls_frontend.add_url_rule('/ingresar', view_func=LoginView.as_view('login'))


@urls_frontend.route('/')
def home():
    return render_template('home.html')


@urls_frontend.route('/salir')
def logout_view():
    session.pop('nombre', None)
    session.pop('tipo', None)
    session.pop('usuario_id', None)
    return redirect(url_for('.login'))
