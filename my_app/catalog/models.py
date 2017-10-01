from my_app import db
from decimal import Decimal
from flask_wtf import Form
from wtforms import TextField, DecimalField, SelectField
from wtforms.validators import InputRequired, NumberRange

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254))
    price = db.Column(db.Float)
    category = db.relationship('Category', backref=db.backref('products', lazy='dynamic'))
    catagory_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    ##Add-on field
    ## company = db.Column(db.String(100))

    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def __repr__(self):
        return '<Product %d>' % self.id

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %d>' % self.id

class ProductForm(Form):
    name = TextField('Name', validators=[InputRequired()])
    price = DecimalField('Price', validators=[
        InputRequired(), NumberRange(min=Decimal('0.0'))
    ])
    category = SelectField('Category', validators=[InputRequired()], coerce=int)
