from app import create_app
from app.extensions import db
from app.common.models import Usuario


app = create_app(app_name='manager')


@app.cli.command()
def init_users():
    """Exec: init-users"""
    admin = Usuario()
    admin.nombre = 'admin'
    admin.contrasena = 'admin'
    admin.tipo = 2
    db.session.add(admin)
    db.session.commit()
    print('ID: ', admin.id)
