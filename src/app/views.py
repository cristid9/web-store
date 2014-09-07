from main import app, db, lm, PRODUCTS_PER_PAGE
from flask import render_template, redirect, session, url_for, request, flash,\
					g, jsonify
from forms import SingupForm, LoginForm
from user import User, PendingUser
from product import Product, Categories
from cart import Cart
from hashlib import md5
from helper import sendMail, generateUrl, flashErrors
from uuid import uuid4
from flask.ext.login import login_user, logout_user, current_user,\
							 login_required

@app.before_request
def before_request():
	g.user = current_user
	g.cart = Cart()
        g.categories = Categories.query.all()

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

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

	flashErrors(form.errors, flash)
	return render_template('singup.html',
		form=form
	)


@app.route('/product_page/<int:productId>')
def productPage(productId=1):
	product = Product.query.get(productId)
	return render_template("product_page.html",
		product=product
	)

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

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
	form =  LoginForm()
	if request.method == "POST" and form.validate():
		user = User.query.filter_by(username=form.username.data, 
			password=md5(form.password.data).hexdigest()
		).first()
		login_user(user)
		flash('User logged in')
		return redirect(url_for('index'))
	
	flashErrors(form.errors, flash)
	return render_template("login.html",
		form=form
	)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
	
@app.route('/categories/<string:category>/<int:page>')
def categories(category, page=1):
	products = Product.query.filter_by(category=category).paginate(page, 
		PRODUCTS_PER_PAGE, False
	)

	return render_template("products.html",
		products=products
	)

@app.route('/add_to_cart', methods=['POST'])
def addToCart():
	productId = request.form["productId"]
	productPrice = request.form["productPrice"]

	g.cart.addToCart(int(productId), float(productPrice))

	print session		
	return jsonify(status="success") 






