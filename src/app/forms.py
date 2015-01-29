## @package forms
#
#  This file will contain all the logical representation of all the forms used
#  in the aplication. 

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, StringField
from wtforms.validators import Required, Email, EqualTo, length, DataRequired
from validators import uniqueUser, validEmail


class SingupForm(Form):
    name = StringField('name', [DataRequired()])
    username = StringField('username', [DataRequired(), uniqueUser])
    email = StringField('email', [validEmail])
    password = PasswordField('password', [
        DataRequired(),
        EqualTo('confirm', message="Parolele nu se potrivesc")
    ])
    confirm = PasswordField('repeat_password')


class LoginForm(Form):
    username = StringField('username', [DataRequired()])
    password = PasswordField('password', [DataRequired()])


class AddressForm(Form):
    phone = StringField('phone', [DataRequired()])
    email = StringField('email', [DataRequired()])
    region = StringField('region', [DataRequired()])
    city = StringField('city', [DataRequired()])
    address = StringField('address', [DataRequired()])


class ContactForm(Form):
    name = StringField('name', [DataRequired()])
    email = StringField('email', [DataRequired()])
    message = TextAreaField('message', [DataRequired(), length(max=500)])


class AddNewProductForm(Form):
    name = StringField('name', [DataRequired()])
    price = StringField('price', [DataRequired()])
    stock = StringField('stock', [StringField()])
    description = TextAreaField('description', [DataRequired()])
    category = StringField('category', [DataRequired()])
    pictures = StringField('pictures', [DataRequired()])
    specifications = StringField('specifications', [DataRequired()])