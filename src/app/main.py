import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask_kvsession import KVSessionExtension
from simplekv.fs import FilesystemStore
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

store = FilesystemStore('./data')

app = Flask(__name__)
KVSessionExtension(store, app)
app.debug = True
app.secret_key = 'kjsdhfssdkf'
app.csrf_enabled = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]

# Setting needed for mail server.
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'XXXXXXXXXXX'
app.config['MAIL_PASSWORD'] = 'XXXXXXXXXXX'
app.config['ADMINS'] = ['XXXXXXXXXXX']

# Create the mai object
mail = Mail(app)

# Initialize the login manager.
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

db = SQLAlchemy(app)

PRODUCTS_PER_PAGE = 10
