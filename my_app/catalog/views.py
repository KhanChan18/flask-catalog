from flask import request, jsonify, Blueprint, render_template, redirect, flash, \
                    url_for
from my_app import app, db
from my_app.catalog.models import Product, Category
from functools import wraps
from flask import flash
from sqlalchemy.orm.util import join
from my_app.catalog.models import ProductForm

catalog = Blueprint('catalog', __name__)

def template_or_json(template=None):
    """"Return a dict from your view and this will either
    pass it to a template or render json. Use like:

    @template_or_json('template.html')
    """
    def decorated(f):
        @wraps(f)
        def decorated_fn(*args, **kwargs):
            ctx = f(*args, **kwargs)
            if request.is_xhr or not template:
                return jsonify(ctx)
            else:
                return render_template(template, **ctx)
        return decorated_fn
    return decorated

@catalog.route('/')
@catalog.route('/home')
@template_or_json('home.html')
def home():
    products = Product.query.all()
    return {'count': len(products)}

@catalog.route('/product/<id>')
def product(id):
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product)

@catalog.route('/products')
@catalog.route('/products/<int:page>')
def products(page=1):
    products = Product.query.paginate(page, 3)
    '''
    res = {}
    for product in products:
        res[product.id] = {
            'name':product.name,
            'price': str(product.price),
            'category': product.category.name
        }
    return jsonify(res)
    '''
    return render_template('products.html', products=products)

@catalog.route('/product-create', methods=['GET','POST'])
def create_product():
    form = ProductForm(request.form, csrf_enabled=False)
    categories = [(c.id, c.name) for c in Category.query.all()]
    form.category.choices = categories

    if form.validate_on_submit():
        name = request.form.get('name')
        price = request.form.get('price')
        category = Category.query.get_or_404(request.form.get('category'))
        product = Product(name, price, category)
        db.session.add(product)
        db.session.commit()
        flash('The product %s has been created' % name, 'success')
        return redirect(url_for('catalog.product', id=product.id))

    if form.errors:
        flash("Some messages you type in need to be fixed.", 'danger')

    return render_template('product-create.html', form=form)

@catalog.route('/category-create', methods=['POST',])
def create_category():
    name = request.form.get('name')
    category = Category(name)
    db.session.add(category)
    db.session.commit()
    return render_template('category.html', category=category)

@catalog.route('/category/<id>')
def category(id):
    category = Category.query.get_or_404(id)
    return render_template('category.html', category=category)

@catalog.route('/categories')
def categories():
    categories = Category.query.all()
    '''
    res = {}
    for category in categories:
        res[category.id] = {
            'name': category.name
        }

        for product in category.products:
            res[category.id]['products'] = {
                'id': product.id,
                'name': product.name,
                'price': product.price
            }
    return jsonify(res)
    '''
    return render_template('categories.html', categories=categories)

@catalog.route('/product-search')
@catalog.route('/product-search/<int:page>')
def product_search(page=1):
    name = request.args.get('name')
    price = request.args.get('price')
    company = request.args.get('company')
    category = request.args.get('category')
    products = Product.query
    if name:
        products = products.filter(Product.name.like('%' + name + '%'))
    if price:
        products = products.filter(Product.price == price)
    if company:
        products = products.filter(Product.company.like('%' + company + '%'))
    if category:
        products = products.select_from(join(Product, Category)).filter(
                Category.name.like('%' + category + '%'))
    return render_template('products.html', products=products.paginate(page, 10))

@catalog.route('/product-admin-submit', methods=['GET','POST'])
def product_admin_submit():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        category = Category.query.get_or_404(request.form.get('category'))
        product = Product(name, price, category)
        db.session.add(product)
        db.session.commit()
        flash('The product %s has been created' % name, 'success')
        return redirect(url_for('catalog.product', id=product.id))
    return render_template('product-create.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
