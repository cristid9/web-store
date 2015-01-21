from main import app, db, lm, PRODUCTS_PER_PAGE
from flask import render_template, redirect, session, url_for, request, flash, \
    g, jsonify, make_response
from forms import SingupForm, LoginForm, AddressForm, ContactForm, AddNewProductForm
from user import User, PendingUser, UserData
from product import Product, Categories
from cart import Cart, ShippingMethods, Order
from hashlib import md5
from helper import sendMail, generateUrl, flashErrors
from uuid import uuid4
from flask.ext.login import login_user, logout_user, current_user, \
    login_required


@app.before_request
def before_request():
    print session
    g.user = current_user
    if not "cart" in session:
        session["cart"] = {}
    if not "shipping" in session:
        session["shipping"] = {"name": None, "price": 0}
    g.cart = Cart(session["cart"], session["shipping"]["price"])
    g.categories = Categories.query.all()
    g.shippingMethods = ShippingMethods.query.all()


@app.route('/')
@app.route('/index')
def index():
    promotionalProducts = Product.query.paginate(1, 3, False)
    return render_template('index.html',
                           promotionalProducts=promotionalProducts)


@app.route('/search', methods=['POST'])
def search():
    products = Product.query.all()
    productsToRender = []
    for product in products:
        if request.form["search"].lower() in product.name.lower() \
                or request.form["search"].lower() in product.description.lower():
            productsToRender.append(product)
    return render_template('search_page.html', products=productsToRender)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST' and form.validate():
        sendMail(subject='Conact',
                 sender=app.config['ADMINS'][0],
                 recipients=app.config['ADMINS'],
                 messageBody='-----',
                 messageHtmlBody=render_template('contact_mail.html',
                                                 email=form.email.data,
                                                 name=form.name.data,
                                                 message=form.message.data)
        )
        return render_template('message_send_successfully.html')

    return render_template('contact.html', form=form)


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
    form = LoginForm()
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(username=form.username.data,
                                    password=md5(form.password.data).hexdigest()
        ).first()
        if not user is None:
            login_user(user)
            flash('Te-ai logat cu succes')
            return redirect(url_for('index'))
        else:
            flash("Numele de utilizator sau parola nu sunt corecte!")
    flashErrors(form.errors, flash)
    return render_template("login.html",
                           form=form
    )


@app.route('/logout')
def logout():
    logout_user()
    del session["cart"]
    del session["shipping"]
    return redirect(url_for('index'))


@app.route('/categories/<string:category>/<int:page>')
def categories(category, page):
    products = Product.query.filter_by(category=category).paginate(page,
                                                                   PRODUCTS_PER_PAGE, False
    )

    return render_template("products.html",
                           products=products
    )


@app.route('/add_new_product', methods=['GET', 'POST'])
def addNewProduct():
    form = AddNewProductForm()
    if request.method == "POST" and form.validate():
        # Add the new product.
        newProduct = Product(form.name.data, float(form.price.data), int(form.stock.data))

        newProduct.category = form.category.data
        newProduct.description = form.description.data

        db.session.add(newProduct)
        db.session.commit()

        # Now that the product has an id we can add the rest of the components.
        # First, if the product's category is not already in the database we should add it.

        if Categories.query.filter_by(name=newProduct.category).first() is None:
            newCategory = Categories(newProduct.category)
            db.session.add(newCategory)
            db.session.commit()

        return str(Categories.query.filter_by(name=newProduct.category).first())

    flashErrors(form.errors, flash)
    return render_template('add_new_product.html',
                           form=form)

@app.route('/add_to_cart', methods=['POST'])
def addToCart():
    product = Product.query.get(int(request.form["productId"]))

    g.cart.addToCart(product.id, product.price)
    session["cart"] = g.cart.items

    print session
    return jsonify(status="success")


@app.route('/cart')
def cart():
    form = AddressForm()
    return render_template("products_in_cart.html",
                           cart=g.cart.getProductData(),
                           form=form
    )


@app.route('/update_cart', methods=['GET', 'POST'])
def updateCart():
    # I think the server should send the total value  to the client. In my
    # opinion the client shouldn't be trusted, even for a small job like
    # this one.

    g.cart.updateQuantity(int(request.form["id"]),
                          int(request.form["quantity"])
    )
    session["cart"] = g.cart.items
    session.modified = True
    app.save_session(session, make_response("dummy"))

    # It's safer to query the database for the product's price.
    product = Product.query.get(int(request.form["id"]))
    return jsonify(total=product.price *
                         int(request.form["quantity"])
    )  # placeholder for real message


@app.route('/check_stock', methods=['GET', 'POST'])
def checkStock():
    product = Product.query.get(int(request.form["id"]))
    return jsonify(stock=product.stock)


@app.route('/get_cart_total', methods=['GET', 'POST'])
def getCartTotal():
    total = g.cart.getTotal()
    return jsonify(total=round(total, 2))


@app.route('/delete_from_cart', methods=['POST'])
def deleteFromCart():
    g.cart.deleteFromCart(int(request.form['id']))
    session["cart"] = g.cart.items
    return jsonify(status="ok")


@app.route('/set_shipping_method', methods=['POST'])
def setShippingMethod():
    # the user will send the method name, update the cart value using the name 
    # of the shiping method

    for shippingMethod in g.shippingMethods:
        if shippingMethod.name == request.form["name"]:
            g.cart.updateShipping(shippingMethod.price)
            session["shipping"]["price"] = g.cart.shipping
            session["shipping"]["name"] = request.form["name"]
            return jsonify(status="ok")
    return jsonify(status="fail")


@app.route('/get_shipping_method', methods=["POST"])
def getShippingMethod():
    return jsonify(name=session["shipping"]["name"])


@app.route('/place_order', methods=["POST"])
def placeOrder():
    form = AddressForm(request.form)
    if form.errors:
        return jsonify(status='fail', errors=form.errors)

    for shippingMethod in g.shippingMethods:
        if shippingMethod.name == request.form["shipping"]:
            g.cart.updateShipping(shippingMethod.price)
    userData = UserData(phone=form.phone.data,
                        email=form.email.data,
                        region=form.region.data,
                        city=form.city.data,
                        address=form.address.data)
    userData.userId = g.user.id
    db.session.add(userData)
    db.session.commit()
    # The third argument was an architerchtural mistake.
    order = Order(g.cart.getTotal(), g.user.id, 1)
    order.address = userData.id
    db.session.add(order)
    db.session.commit()

    cart = []
    for item in g.cart.items:
        cart.append({
            'quantity': g.cart.items[item]['quantity'],
            'name': Product.query.get(item).name,
            'price': g.cart.items[item]['price']
        })

    sendMail(subject='Factura',
             sender=app.config['ADMINS'][0],
             recipients=[form.email.data, app.config['ADMINS'][0]],
             messageBody='----',
             messageHtmlBody=render_template('bill.html',
                                             cart=cart,
                                             name=g.user.name,
                                             total=g.cart.getTotal(),
                                             phone=form.phone.data,
                                             region=form.region.data,
                                             city=form.city.data,
                                             address=form.address.data,
                                             shipping=request.form['shipping'],
                                             shippingCost=ShippingMethods.query.filter_by(
                                                 name=request.form['shipping']).first().price)
    )


    # Reset the cart.
    session["cart"] = {}

    return jsonify(status="ok")


