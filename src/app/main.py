from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.secret_key = 'kjsdhfssdkf'
db = SQLAlchemy(app)


