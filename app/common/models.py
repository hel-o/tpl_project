from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.common.constants import TipoUsuario


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False, unique=True)
    contrasena_hash = db.Column(db.String(250), nullable=False)
    tipo = db.Column(db.Integer, nullable=False, default=TipoUsuario.ADMIN)
    estado = db.Column(db.CHAR(1), nullable=False, default='A')  # activo

    @property
    def contrasena(self):
        raise AttributeError('password is not a readable attribute')

    @contrasena.setter
    def contrasena(self, contrasena):
        self.contrasena_hash = generate_password_hash(contrasena)

    @staticmethod
    def validar_usuario(nombre, contrasena):
        user = Usuario.query.filter_by(nombre=nombre).first()
        if user:
            if check_password_hash(user.contrasena_hash, contrasena):
                return user
        return None

    def to_json(self):
        return {
            'id': self.id,
            'estado': self.estado,
            'nombre': self.nombre
        }
