from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, Email

class RequestForm(Form):
	address = StringField("Address", validators=[DataRequired("Please enter an address.")])
	zipcode = StringField("Zip Code", validators=[DataRequired("Please enter your zip code."), Length(min=5, message="Zip code must be 5 numbers")])
	service_code = IntegerField(validators=[DataRequired("Please enter service code.")])
	service_name = StringField("Service Name", validators=[DataRequired("Please enter service name.")])
	description = StringField("What is the problem description", validators=[DataRequired("Please enter problem description.")])
	request_date = StringField("Today's Date", validators=[DataRequired("Please enter today's date.")])
	submit = SubmitField("Submit!")

class SignupForm(Form):
	first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
	last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
	email = StringField('Email', validators=[DataRequired("Please enter your email."), Email("Please enter a valid email.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=8, message="Passwords must be 8 characters or more.")])
	submit = SubmitField('Sign up') 

class SignInForm(Form):
	email = StringField('Email', validators=[DataRequired("Please enter your email address"), Email("Please enter your email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])
	submit = SubmitField("Sign in")