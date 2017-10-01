from my_app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254))
    price = db.Column(db.Float)
    category = db.relationship('Category', backref=db.backref('products', lazy='dynamic'))
    catagory_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    ##Add-on field
    company = db.Column(db.String(100))

    def __init__(self, name, price, category, company):
        self.name = name
        self.price = price
        self.category = category
        self.company = company

    def __repr__(self):
        return '<Product %d>' % self.id

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %d>' % self.id
