from main import app, db
from flask import render_template, redirect, session, url_for, request, flash
from forms import SingupForm
from user import User
from hashlib import md5

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
		newUser = User(name=form.name.data, username=form.username.data,
						   password=md5(form.password.data).hexdigest(), 
						   email=form.email.data)

		db.session.add(newUser)
		db.session.commit()
		flash("User " + form.name.data + " was added")
	else:
		flash("Form is invalid")

	return render_template('singup.html',
		form=form
	)


@app.route('/product_page/<int:product_id>')
def product_page(product_id=1):
	pass
