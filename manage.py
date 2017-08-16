from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from app.common.models import Usuario
from app.module1.models import Modelname


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


def init_users():
    admin = Usuario()
    admin.nombre = 'admin'
    admin.contrasena = 'admin'
    admin.tipo = 'A'
    db.session.add(admin)
    db.session.commit()
    print('user ADMIN created!, with id: ', admin.id)

manager.command(init_users)


if __name__ == '__main__':
    manager.run()
