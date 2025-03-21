from flask import Flask, render_template, url_for, redirect, request, flash, make_response
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import DeclarativeBase
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

from flask import session, redirect, url_for, flash


class Base(DeclarativeBase):
    pass


app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXdgfox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

#login
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    sizes = db.Column(db.String, nullable=False)
    colors = db.Column(db.String, nullable=False)
    original_price = db.Column(db.Float, nullable=False)
    productInfo = db.Column(db.Text, nullable=False)
    imgUrl1 = db.Column(db.String(200), nullable=False)
    imgUrl2 = db.Column(db.String(200))
    imgUrl3 = db.Column(db.String(200))
    imgUrl4 = db.Column(db.String(200))
    category = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Product {self.title}>'


#login user and login form
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


with app.app_context():
    db.create_all()


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('admin'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    session.clear()  # Clear all session data
    flash('You have been logged out.', 'info')
    return redirect(url_for('shop'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    sort_order = request.args.get('sort', 'asc')  # Default to 'asc' if not provided
    category = request.args.get('category', None)
    price_range = request.args.get('price', None)
    print(price_range)
    # Fetch products from the database and apply filters
    products_query = Product.query

    if category:
        print(category)
        products_query = products_query.filter_by(category=category)

    if price_range:
        min_price, max_price = map(float, price_range.split('-'))
        products_query = products_query.filter(Product.original_price.between(min_price, max_price))
    if sort_order == 'desc':
        products = products_query.order_by(Product.price.desc()).all()
    else:
        products = products_query.order_by(Product.price.asc()).all()

    return render_template('shop.html', products=products, sort_order=sort_order, category=category,
                           price_range=price_range)


@app.route('/page')
def shop_product():
    return render_template('shop-details.html')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('shop'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/item/<int:id>')
def item(id):
    product = Product.query.get_or_404(id)
    return render_template("shop-details.html", product=product)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Process any server-side logic if needed
        return '', 204  # No content response
    return render_template('contact.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


Bootstrap(app)


class AdminForm(FlaskForm):
    title = StringField('Product Title', validators=[DataRequired()], render_kw={"placeholder": "Solid Blue T-Shirt"})
    description = TextAreaField('Product Description', validators=[DataRequired()],
                                render_kw={"placeholder": "Enter product description"})
    price = FloatField('Discounted Price', validators=[DataRequired()], render_kw={"placeholder": "₹499"})
    original_price = FloatField('Original Price', validators=[DataRequired()], render_kw={"placeholder": "₹699"})
    category = SelectField('Category', choices=['Men', 'Women', 'Bags', 'Shoes', 'Accessories', 'Kids'],
                           validators=[DataRequired()])
    imgURL1 = StringField('Image URL 1', validators=[DataRequired()], render_kw={"placeholder": "Required"})
    imgURL2 = StringField('Image URL 2')
    imgURL3 = StringField('Image URL 3')
    imgURL4 = StringField('Image URL 4')
    sizes = StringField('Sizes (comma separated)', validators=[DataRequired()], render_kw={"placeholder": "XS,S,L,XL"})
    colors = StringField('Colors (comma separated)', validators=[DataRequired()],
                         render_kw={"placeholder": "Black,Blue,Red,Yellow"})
    submit = SubmitField('Add Product')


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    form = AdminForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        price = form.price.data
        original_price = form.original_price.data
        category = form.category.data
        imgURL1 = form.imgURL1.data
        imgURL2 = form.imgURL2.data
        imgURL3 = form.imgURL3.data
        imgURL4 = form.imgURL4.data
        sizes = form.sizes.data
        colors = form.colors.data
        new_product = Product(
            title=title,
            productInfo=description,
            price=price,
            original_price=original_price,
            category=category,
            imgUrl1=imgURL1,
            imgUrl2=imgURL2,
            imgUrl3=imgURL3,
            imgUrl4=imgURL4,
            sizes=sizes,
            colors=colors,
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('all'))

    response = make_response(render_template('admin.html', form=form))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    return response


@app.route('/search', methods=['GET', 'POST'])
def search():
    return redirect(url_for('shop'))


@app.route('/admin/all')
@login_required
def all():
    products = Product.query.all()
    return render_template('allproducts.html', products=products)


@app.route('/faq')
def faq():
    return render_template('faq.html')


if __name__ == '__main__':
    app.run(debug=True)
