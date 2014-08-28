from main import app, db
from flask import render_template, redirect, session, url_for, request, flash
from forms import SingupForm
from user import User, PendingUser
from hashlib import md5
from helper import sendMail, generateUrl
from uuid import uuid4

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
		newPendingUser = PendingUser(pendingId=str(uuid4()),
			name=form.name.data,
			username=form.username.data,
			password=md5(form.password.data).hexdigest(), 
			email=form.email.data
		)

		db.session.add(newPendingUser)
		db.session.commit()
		
		mailUrl = generateUrl(    
			route=url_for('validateUser', 
				pendingUserId=newPendingUser.pendingId
			),
			hostname=request.host
		)

		sendMail(subject="Validation Mail",
			sender=app.config['ADMINS'][0],
			recipients=[newPendingUser.email],
			messageBody=render_template("confirmation_mail_body.html", 
				confirmationLink=mailUrl			
			),
			messageHtmlBody=render_template(
				"confirmation_mail_html_body.html",
				confirmationLink=mailUrl
			)
		)
		

		flash("User " + form.name.data + " was added")

		return render_template("before_finish_singup.html",
			 email=form.email.data
		)

	for error in form.errors:
		for fieldError in form.errors[error]:
			flash(error + fieldError)

	return render_template('singup.html',
		form=form
	)


@app.route('/product_page/<int:product_id>')
def product_page(product_id=1):
	pass


@app.route('/validate/<pendingUserId>')
def validateUser(pendingUserId):
	pendingUser = PendingUser.query.filter_by(pendingId=pendingUserId).first()
	if pendingUser is None:
		return render_template("invalid_activation_link.html")

	user = User(name=pendingUser.name,
		email=pendingUser.email,
		password=pendingUser.password,
		username=pendingUser.username
	)

	db.session.add(user)
	db.session.delete(pendingUser)
	db.session.commit()

	return render_template("successfull_activation.html", 
		username=user.username
	)





