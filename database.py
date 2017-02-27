from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import random

db = SQLAlchemy()

class serviceRequest(db.Model):
	__tablename__ = 'Service Requests'
	address = db.Column(db.String(200), primary_key=True)
	zipcode = db.Column(db.String(5))
	service_code = db.Column(db.Integer)
	service_name = db.Column(db.String(200))
	service_request_id = db.Column(db.Integer)
	description = db.Column(db.String(300))
	status = db.Column(db.String(100))
	status_notes = db.Column(db.String(300))
	request_date = db.Column(db.String(150))
	update_date = db.Column(db.String(150))
	expected_date = db.Column(db.String(150))
	agency_responsible = db.Column(db.String(250))

	def __init__(self, address, zipcode, service_code, service_name, service_request_id, description, status, status_notes, request_date, update_date, expected_date, agency_responsible):
		self.address = address.title()
		self.zipcode = zipcode
		self.service_code = service_code
		self.service_name = service_name.title()
		self.service_request_id = service_request_id
		self.description = description.title()
		self.status = status.title()
		self.status_notes = status_notes.title()
		self.request_date = request_date.title()
		self.update_date = update_date.title()
		self.expected_date = expected_date.title()
		self.agency_responsible = agency_responsible.title()

class Admin(db.Model):
	__tablename__ = 'admin'
	adminid = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120))
	pwdhash = db.Column(db.String(54))

	def __init__(self, firstname, lastname, email, password):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)


class Users(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120))
	pwdhash = db.Column(db.String(54))

	def __init__(self, firstname, lastname, email, password):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)