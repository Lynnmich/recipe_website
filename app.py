import os
from os import environ, path
from flask import Flask, render_template, flash, redirect, request, url_for
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_migrate import Migrate
import werkzeug
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from forms import RecipeForm, LoginForm, AdminForm, SearchForm
from flask_paginate import get_page_args, Pagination

app = Flask(__name__)
ckeditor = CKEditor(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'recipes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "key"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_admin(admin_id):
    return Admin.query.get(int(admin_id))


'''# Create a Category model
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    recipes = relationship("Recipe", back_populates="category")'''


# Create a Recipe model
class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.Date, default=date.today)
    slug = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    preparation_time = db.Column(db.String(20), nullable=False)
    cooking_time = db.Column(db.String(20), nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    energy = db.Column(db.String(20), nullable=False)
    protein = db.Column(db.String(20), nullable=False)
    fat = db.Column(db.String(20), nullable=False)
    fiber = db.Column(db.String(20), nullable=False)
    vitamin_a = db.Column(db.String(20), nullable=False)
    iron = db.Column(db.String(20), nullable=False)
    zinc = db.Column(db.String(20), nullable=False)
    carbohydrate = db.Column(db.String(20), nullable=False)
    upvotes = db.Column(db.Integer)
    '''category_id = db.Column(db.Integer, db.ForeignKey('categories.id', name='fk_category_id'))  # Add name here
    category = db.relationship("Category", back_populates="recipes")'''


# Create an Admin Model
class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    admin_name = db.Column(db.String(20), nullable=False, unique=True)
    date_added = db.Column(db.Date, default=date.today)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# Route Decorators
@app.route('/')
def index():
    return render_template("index.html")


def get_page():
    return request.args.get('page', 1, type=int)


def paginate_list(query, page_number, per_page):
    array = [item for item in query]
    paginated_array = array[((page_number*per_page)-per_page):(page_number*per_page)]
    return paginated_array


# All Recipes
@app.route('/recipes')
def recipes():
    # Fetch the page, per_page, and offset from the request
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    # Query all recipes
    query = Recipe.query


    # Count the total number of recipes
    total = query.count()

    # Paginate the query
    recipes = query.order_by(Recipe.date_posted).offset(offset).limit(per_page).all()

    # Create a Pagination object
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap4')

    return render_template("recipes.html", recipes=recipes, pagination=pagination)

# One Recipe
@app.route('/recipes/<int:id>')
def recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe.html', recipe=recipe)


# Add a recipe
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()

    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            subtitle=form.subtitle.data,
            slug=form.slug.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            preparation_time=form.preparation_time.data,
            cooking_time=form.cooking_time.data,
            servings=form.servings.data,
            energy=form.energy.data,
            protein=form.protein.data,
            fat=form.fat.data,
            fiber=form.fiber.data,
            vitamin_a=form.vitamin_a.data,
            iron=form.iron.data,
            zinc=form.zinc.data,
            carbohydrate=form.carbohydrate.data
        )

        form.title.data = ''
        form.subtitle.data = ''
        form.slug.data = ''
        form.ingredients.data = ''
        form.instructions.data = ''
        form.preparation_time.data =''
        form.cooking_time.data=''
        form.servings.data=''
        form.energy.data = ''
        form.protein.data = ''
        form.fat.data = ''
        form.fiber.data = ''
        form.vitamin_a.data = ''
        form.iron.data = ''
        form.zinc.data = ''
        form.carbohydrate.data = ''

        #Add and Commit recipe to the database
        db.session.add(recipe)
        db.session.commit()

        flash("Recipe added successfully!")

    return render_template("add_recipe.html", form=form)


# Edit a recipe
@app.route('/recipes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    form = RecipeForm()

    if request.method == 'POST' and form.validate():
        recipe.title = form.title.data
        recipe.subtitle = form.subtitle.data
        recipe.slug = form.slug.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        recipe.preparation_time = form.preparation_time.data
        recipe.cooking_time = form.cooking_time.data
        recipe.servings = form.servings.data
        recipe.energy = form.energy.data
        recipe.protein = form.protein.data
        recipe.fat = form.fat.data
        recipe.fiber = form.fiber.data
        recipe.vitamin_a = form.vitamin_a.data
        recipe.iron = form.iron.data
        recipe.zinc = form.zinc.data
        recipe.carbohydrate = form.carbohydrate.data

        db.session.commit()

        flash("Recipe updated successfully!")
        return redirect(url_for("recipe", id=recipe.id))

    # Prepopulate the form fields with the existing recipe data
    form.title.data = recipe.title
    form.subtitle.data = recipe.subtitle
    form.slug.data = recipe.slug
    form.ingredients.data = recipe.ingredients
    form.instructions.data = recipe.instructions
    form.preparation_time.data = recipe.preparation_time
    form.cooking_time.data = recipe.cooking_time
    form.servings.data = recipe.servings
    form.energy.data = recipe.energy
    form.protein.data = recipe.protein
    form.fat.data = recipe.fat
    form.fiber.data = recipe.fiber
    form.vitamin_a.data = recipe.vitamin_a
    form.iron.data = recipe.iron
    form.zinc.data = recipe.zinc
    form.carbohydrate.data = recipe.carbohydrate

    return render_template('edit_recipe.html', form=form)


# Delete a recipe
@app.route('/recipes/delete/<int:id>')
@login_required
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)

    try:
        db.session.delete(recipe)
        db.session.commit()

        flash("Recipe deleted!")

    except:
        flash("There was a problem deleting the recipe")

    return redirect(url_for("recipes"))


# Create an Admin page
@app.route('/admin')
def admin():
    # Retrieve all admins from the database
    admin = Admin.query.order_by(Admin.id)
    return render_template("admin.html", admin=admin)


# Add Admin
@app.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    name = None
    form = AdminForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin is None:
            hashed_password = generate_password_hash(form.password_hash.data, 'sha256')
            admin = Admin(name=form.name.data, admin_name=form.admin_name.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(admin)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.admin_name.data = ''
        form.email.data = ''
        form.password_hash.data =''

        flash("Admin added successfully!")
        my_admin = Admin.query.order_by(Admin.id)
        return render_template("add_admin.html", form=form, name=name, my_admin=my_admin)
    
    return render_template("add_admin.html", form=form, name=name)


# Delete Admin
@app.route('/admin/delete/<int:id>')
def delete_admin(id):
    admin_delete = Admin.query.get_or_404(id)

    try:
        db.session.delete(admin_delete)
        db.session.commit()

        flash("Admin deleted!")

        # Return all admins from the db
        admin = Admin.query.order_by(Admin.date_added)
        return render_template("admin.html", admin=admin)

    except:
        # Error message
        flash("There was a problem deleting the admin")

        # Return all admins from the db
        admin = Admin.query.order_by(Admin.date_added)
        return render_template("admin.html", admin=admin)


# Update Database
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    name_to_update = Admin.query.get_or_404(id)
    form = AdminForm(obj=name_to_update)
    if form.validate_on_submit():
        name_to_update.name = form.name.data
        name_to_update.email = form.email.data
        name_to_update.password = form.password_hash.data

        try:
            db.session.commit()
            flash('Admin credentials updated successfully!')
            return redirect(url_for('admin'))
        except:
            flash('Oops! There was an error updating Admin credentials')

    return render_template("update.html", form=form, name_to_update=name_to_update)


# Search for a recipe
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    recipes = Recipe.query
    if form.validate_on_submit():
        recipe.searched = form.searched.data
        recipes = recipes.filter(Recipe.title.like('%' + recipe.searched + '%'))
        recipes = recipes.order_by(Recipe.title).all()
        return render_template("search.html", form=form, searched=recipe.searched, recipes=recipes)


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(admin_name=form.admin_name.data).first()
        if admin:
            if check_password_hash(admin.password_hash, form.password.data):
                login_user(admin)
                flash("Logged in Successfully!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password. Please try again")
        else:
            flash("Admin doesn't exist")

    return render_template('login.html', form=form)


# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Retrieve all recipes from the database
    recipes = Recipe.query.order_by(Recipe.date_posted).all()
    return render_template('dashboard.html', recipes=recipes)


# Logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully")
    return redirect(url_for('login'))


# Information about the recipes
@app.route('/info')
def info():
    return render_template("info.html")


@app.route('/upvote/<int:recipe_id>', methods=["POST"])
def upvote(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        recipe.upvotes = (recipe.upvotes or 0) + 1
        db.session.commit()
        return redirect(url_for('recipe', id=recipe.id))
    else:
        return render_template("404.html"), 404


# Pass information to the navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# Custom Error page decorator
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run()
