from main import app
from flask import render_template, redirect, session, url_for, request
from froms import SingupForm

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/login')
def login():
	pass

@app.route('/singup', methods=['GET', 'POST'])
def singup():
	form = SingupForm(request.form)
	
	if request.method == 'POST' and form.validate():
		pass

	return render_template('singup.html',
		form=form
	)


@app.route('/product_page/<product_id:int>')
def product_page(product_id=1):
	pass
