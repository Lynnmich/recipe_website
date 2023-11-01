
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, widgets, PasswordField, BooleanField, SelectField, IntegerField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed


# Create a Recipe Form
class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    ingredients = CKEditorField('Ingredients', validators=[DataRequired()])
    instructions = CKEditorField('Instructions', validators=[DataRequired()])
    preparation_time = StringField('Preparation Time', validators=[DataRequired()])
    cooking_time = StringField('Cooking Time', validators=[DataRequired()])
    servings = IntegerField('Servings', validators=[DataRequired()])
    energy = StringField('Energy', validators=[DataRequired()])
    protein = StringField('Protein', validators=[DataRequired()])
    fat = StringField('Fat', validators=[DataRequired()])
    fiber = StringField('Fiber', validators=[DataRequired()])
    vitamin_a = StringField('Vitamin A', validators=[DataRequired()])
    iron = StringField('Iron', validators=[DataRequired()])
    zinc = StringField('Zinc', validators=[DataRequired()])
    carbohydrate = StringField('Carbohydrate', validators=[DataRequired()])
    

    submit = SubmitField("Submit")


'''# Create a Category Form
class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField("Submit")'''

# Create an Admin Form
class AdminForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    admin_name = StringField("Admin_name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match!')])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a Login Form
class LoginForm(FlaskForm):
    admin_name = StringField("Admin_name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
     

# Create a Search Form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Search")