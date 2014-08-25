from main import app
from flask import render_template, redirect, session, url_for

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/login')
def login():
	pass
