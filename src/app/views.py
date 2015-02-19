import json
from main import app, db, lm, PRODUCTS_PER_PAGE
from flask import render_template, redirect, session, url_for, request, flash, \
    g, jsonify, make_response
from forms import SingupForm, LoginForm, AddressForm, ContactForm, AddNewProductForm, AddShippingMethodForm
from user import User, PendingUser, UserData
from product import Product, Categories, ProductPictures, ProductComment, ProductSpecifications
from cart import Cart, ShippingMethods, Order, ProductsInOrder
from hashlib import md5
from decorators import isAdmin
from helper import sendMail, generateUrl, flashErrors
from uuid import uuid4
from flask.ext.login import login_user, logout_user, current_user, \
    login_required


@app.before_request
def before_request():
    print session
    g.user = current_user
    if "cart" not in session:
        session["cart"] = {}
    if "shipping" not in session:
        session["shipping"] = {"name": None, "price": 0}
    g.cart = Cart(session["cart"], session["shipping"]["price"])
    g.categories = Categories.query.filter(Categories.available == True).all()
    g.shippingMethods = ShippingMethods.query.all()


@app.route('/')
@app.route('/index')
def index():
    product_query = Product.query.filter(Product.available == True)
    promotional_products = product_query.paginate(1, 3, False)
    return render_template('index.html',
                           promotionalProducts=promotional_products,
                           active_page=url_for('index'))


@app.route('/search', methods=['POST'])
def search():
    products = Product.query.filter(Product.available == True).all()
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

    return render_template('contact.html',
                           form=form,
                           active_page=url_for('contact'))


@app.route('/singup', methods=['GET', 'POST'])
def singup():
    form = SingupForm(request.form)

    if request.method == 'POST' and form.validate():
        newPendingUser = PendingUser(pendingId=str(uuid4()),
                                     name=form.name.data,
                                     username=form.username.data,
                                     password=md5(form.password.data).hexdigest(),
                                     email=form.email.data)

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
                           form=form)

@app.route('/user_page/<string:user_name>', methods=['GET'])
def user_page(user_name):
    user = User.query.filter_by(username=user_name).first()

    active_page = url_for('user_page', user_name=user_name)
    return render_template('user_page.html',
                           user=user,
                           active_page=active_page)


@app.route('/product_page/<int:productId>')
def productPage(productId=1):
    product = Product.query.get(productId)
    if product is None:
        return render_template("product_does_not_exists.html")
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
                state="normal",
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
    query = Product.query.filter(Product.category == category,
                                 Product.available == True)
    products = query.paginate(page, PRODUCTS_PER_PAGE, False)

    # The content doesn't really matter, he important thing is
    # to make sure if we are indeed on this page.
    return render_template("products.html",
                           products=products,
                           active_page="categories")

@app.route('/add_new_product', methods=['GET', 'POST'])
@login_required
@isAdmin(route="onlyAdmins")
def addNewProduct():
    form = AddNewProductForm()
    if request.method == "POST" and form.validate():
        # Add the new product.
        newProduct = Product(form.name.data, float(form.price.data), int(form.stock.data))

        newProduct.category = form.category.data
        newProduct.description = form.description.data

        db.session.add(newProduct)
        db.session.commit()

        # We should, also, add the product specifications.
        # Specifications are sent as a json string. We do this because it
        # is really hard to generate dynamic for fields on the client with wtforms.
        # The solution is to have a single string field generated with wtforms and
        # to simulate the rest of the string fields on the client, when the client
        # will submit the form, the values of that fields will be collected and saved
        # in that master field. We use a javascript object on the client to track
        # the fields an their values, so at the submission the master field will
        # contain the json representation of that object.
        specifications = json.loads(form.specifications.data)

        for spec_name, spec_value in specifications.iteritems():
            db.session.add(ProductSpecifications(newProduct.id, spec_name, spec_value))
        db.session.commit()

        # Now add the images.
        pictures = form.pictures.data.split('|')
        del pictures[-1]

        for pictureLink in pictures:
            db.session.add(ProductPictures(pictureLink, newProduct.id))
        db.session.commit()

        # Now that the product has an id we can add the rest of the components.
        # First, if the product's category is not already in the database we should add it.
        category = Categories.query.filter_by(name=newProduct.category).first()
        if category is None:
            newCategory = Categories(newProduct.category)
            db.session.add(newCategory)
            db.session.commit()

        # The product category may exist, but is unavailable, because there
        # are no products available left in it. We should make it available.
        if not category.available:
            category.available = True
            db.session.add(category)
            db.session.commit()

        return redirect(url_for('productAddedSuccessfully', name=newProduct.name))

    flashErrors(form.errors, flash)
    return render_template('add_new_product.html',
                           form=form)


@app.route('/only_admins', methods=['GET'])
def onlyAdmins():
    return render_template('only_admins.html')


@app.route('/product_added_successfully/<string:name>', methods=['GET'])
def productAddedSuccessfully(name):
    return render_template('product_added_successfully.html',
                           name=name)


@app.route('/add_to_cart', methods=['POST'])
def addToCart():
    print "*" * 70
    print request.form["productId"]
    print "*" * 70
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
                           is_empty = g.cart.is_empty(),
                           form=form,
                           active_page=url_for('cart'))

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
                   int(request.form["quantity"]))

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
    # of the shipping method

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

    order = Order(g.cart.getTotal(), g.user.id, userData.id)
    db.session.add(order)
    db.session.commit()

    # Now add the products in the cart.
    for product_id in g.cart.get_products_ids():
        db.session.add(ProductsInOrder(product_id,
                                       order.id,
                                       g.cart.get_quantity_by_id(product_id)))
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

@app.route('/change_user_name', methods=['POST'])
def change_user_name():
    if g.user.is_authenticated():
        g.user.name = request.form["newName"]

        db.session.add(g.user)
        db.session.commit()

        return jsonify(status="ok")

    return jsonify(status="not authenticated")


@app.route('/change_user_email', methods=['POST'])
def change_user_email():
    # This condition is to prevent people to send json with the new
    # email, even if the account is not theirs
    if g.user.is_authenticated():
        g.user.email = request.form['newEmail']

        db.session.add(g.user)
        db.session.commit()

        return jsonify(status="ok")

    return jsonify(status="not authenticated")

@app.route('/check_password', methods=['POST'])
@login_required
def check_password():
    if g.user.password != md5(request.form["currentPassword"]).hexdigest():
        return jsonify(status="wrong")
    return jsonify(status="correct")

@app.route('/change_password', methods=['POST'])
def change_password():
    if g.user.is_authenticated():
        g.user.password = md5(request.form["newPassword"]).hexdigest()

        # Save the changes to the database.
        db.session.add(g.user)
        db.session.commit()

        return jsonify(status="ok")
    return jsonify(status="not authenticated")

@app.route("/delete_product", methods=["Post"])
@login_required
@isAdmin(route='onlyAdmins')
def delete_product():
    product = Product.query.get(int(request.form["productId"]))
    product.available = False

    db.session.add(product)
    db.session.commit()

    products_in_category = Product.query.filter_by(category=product.category,
                                                   available=True)
    num_products_in_category = len(products_in_category.all())
    if num_products_in_category == 0:
        category = Categories.query.filter_by(name=product.category).first()
        category.available = False

        db.session.add(category)
        db.session.commit()

    # \todo do a migrate
    # \todo check the availability of an product and a category before using it.

    return jsonify(status="ok")

@app.route("/product_deleted_successfully", methods=["GET"])
def product_deleted_successfully():
    return render_template("product_deleted_successfully.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/edit_product/<int:product_id>", methods=['GET', 'POST'])
@login_required
@isAdmin(route="onlyAdmins")
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = AddNewProductForm()

    if request.method == "POST" and form.validate():
        product.name = form.name.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.category = form.category.data
        product.description = form.description.data

        # Delete the old images.
        for picture in product.pictures:
            db.session.delete(picture)
        db.session.commit()

        # Now add the new ones.
        new_pictures_urls = json.loads(form.pictures.data)
        for picture_url in new_pictures_urls:
            db.session.add(ProductPictures(picture_url, product.id))
        db.session.commit()

        # Delete the old specifications.
        for spec in product.specifications:
            db.session.delete(spec)
        db.session.commit()

        # Now add the new ones.
        new_specs = json.loads(form.specifications.data)
        for spec_name, spec_val in new_specs.iteritems():
            db.session.add(ProductSpecifications(product.id, spec_name, spec_val))
        db.session.commit()

        return redirect('product_edited_successfully')

    # It is impossible to set the value of a text area at
    # render time.
    form.description.data = product.description
    return render_template("edit_product.html",
                           form = form,
                           product = product)

@app.route("/product_edited_successfully", methods=["GET"])
def product_edited_successfully():
    return render_template("product_edited_successfully.html")

@app.route("/add_shipping_method", methods=["GET", "POST"])
@login_required
@isAdmin(route="onlyAdmins")
def add_shipping_method():
    form = AddShippingMethodForm()

    if request.method == "POST" and form.validate():
        new_shipping_method = ShippingMethods(form.name.data,
                                              form.price.data,
                                              form.delivery_time.data,
                                              form.area.data)

        db.session.add(new_shipping_method)
        db.session.commit()

        return redirect(url_for('shipping_method_added_successfully'))

    else:
        flashErrors(form.errors, flash)

    return render_template("add_shipping_method.html",
                           form=form)

@app.route("/shipping_method_added_successfully", methods=["GET"])
def shipping_method_added_successfully():
    return render_template("shipping_method_added_successfully.html")

@app.route("/ban_user", methods=["POST"])
@login_required
@isAdmin(route="onlyAdmins")
def ban_user():
    username = request.form["user"]
    admin = request.form["admin"]
    user = User.query.filter_by(username=username).first()

    # Send an email to the user and tell him that you have
    # deleted his account.

    sendMail(subject="Your account has been deleted",
             sender=app.config['ADMINS'][0],
             recipients=[user.email],
             messageBody=render_template('deleted_account.txt',
                                         user=user.name,
                                         admin=admin),
             messageHtmlBody=render_template('deleted_account.html',
                                             user=user.name,
                                             admin=admin))

    # Now delete the user.
    db.session.delete(user)
    db.session.commit()

    return jsonify(status="ok",
                   redirectPage=url_for('user_deleted_successfully'))

@app.route('/user_deleted_successfully', methods=["GET"])
@login_required
@isAdmin(route="onlyAdmins")
def user_deleted_successfully():
    return render_template('user_deleted_successfully.html')

@app.route('/bought_products/<string:username>', methods=['GET'])
@login_required
def bought_products(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        return render_template('no_access.html')

    if user.id != g.user.id:
        return render_template('no_access.html')

    orders = Order.query.filter_by(user_id=user.id).all()

    return render_template('bought_products.html',
                           orders=orders)
