from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
##from flask_restful import Api
import os

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/my_app/static/uploads'
app.secret_key = 'GNU is Not Unix'
app.debug = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
##api = Api(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from my_app.catalog.views import catalog
app.register_blueprint(catalog)

db.create_all()
