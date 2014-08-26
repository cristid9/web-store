from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.secret_key = 'kjsdhfssdkf'
app.csrf_enabled = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://cristi:1234@localhost/"\
										"test_web_store_db"

db = SQLAlchemy(app)


