from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, PasswordField, BooleanField,EmailField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Edit Profile')

class LoginForm(FlaskForm) : 
    """Login Form""" 
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()]) 
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In') 

class RegisterForm(FlaskForm) : 
    """register Form""" 
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    email= EmailField('Email', validators=[DataRequired()]) 
    password = PasswordField('Password', validators=[DataRequired()]) 
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()]) 
    submit = SubmitField('Register') 

class AddproductForm(FlaskForm) : 
    """Add product Form""" 
    product_name = StringField('Product Name', validators=[DataRequired(), Length(1, 64)])
    product_description = StringField('Product Description', validators=[DataRequired(), Length(1, 64)]) 
    stock_available= SelectField('Stock Available',  choices=[],validators=[DataRequired()]) 
    submit = SubmitField('Add Product')  

    # defining a range of numbers for the selectfield
    def __init__(self, *args, **kwargs):
        super(AddproductForm, self).__init__(*args, **kwargs)
        self.stock_available.choices = [(str(i), str(i)) for i in range(1, 21)]  #defines a range  from 1 to 20     

class PostForm(FlaskForm):
   """Comment form"""
   body = TextAreaField('Body', validators=[DataRequired()]) 
   submit = SubmitField('Post')