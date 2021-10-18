# Пока не готово 18 10 21
from flask import Flask
from rct import models
from flask_migrate import Migrate
from flask_script import Manager

from rct.models import db

app = Flask(__name__, instance_relative_config=True)
migrate = Migrate(app, db)
manager = Manager(app)

# Читаем config
app.config.from_pyfile("config_ins.py")

# Инициализируем объект приложения
db.init_app(app)

# создать экземпляр класса Migrate, передав экземпляр приложения (app) и объект SQLAlchemy (db)
migrate = Migrate(app, db)



manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()