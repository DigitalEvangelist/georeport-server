"""
    GeoReport v2 Server
    -------------------

    Open311 GeoReport v2 Server implementation written in Flask.

    :copyright: (c) Miami-Dade County 2011
    :author: Julian Bonilla (@julianbonilla)
    :license: Apache License v2.0, see LICENSE for more details.
"""
from data import service_types, service_definitions, service_discovery, srs
from flask import Flask, render_template, request, abort, json, jsonify, make_response, redirect, url_for
from database import db, serviceRequest, Admin, Users
from forms import RequestForm, SignupForm, SignInForm
import random

# Configuration
DEBUG = True
ORGANIZATION = 'Miami-Dade County'
JURISDICTION = 'miamidade.gov'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('GEOREPORT_SETTINGS', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/schenectadyOpen311'
db.init_app(app)
app.secret_key = "development-key"

@app.route('/')
def index():
    return render_template('initial.html', org=app.config['ORGANIZATION'], 
                           jurisdiction=app.config['JURISDICTION'])


@app.route('/discovery.<format>')
def discovery(format):
    """Service discovery mechanism required for Open311 APIs."""
    if format == 'json':
        return jsonify(service_discovery)
    elif format == 'xml':
        response = make_response(render_template('discovery.xml', discovery=service_discovery))
        response.headers['Content-Type'] = 'text/xml; charset=utf-8'
        return response
    else:
        abort(404)


@app.route('/services.<format>')
def service_list(format):
    """Provide a list of acceptable 311 service request types and their 
    associated service codes. These request types can be unique to the
    city/jurisdiction.
    """
    if format == 'json':
        response = make_response(json.dumps(service_types))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    elif format == 'xml':
        response = make_response(render_template('services.xml', services=service_types))
        response.headers['Content-Type'] = 'text/xml; charset=utf-8'
        return response
    else:
        abort(404)


@app.route('/services/<service_code>.<format>')
def service_definition(service_code, format):
    """Define attributes associated with a service code.
    These attributes can be unique to the city/jurisdiction.
    """
    if service_code not in service_definitions:
        abort(404)

    if format == 'json':
        return jsonify(service_definitions[service_code])
    elif format == 'xml':
        response = make_response(render_template('definition.xml',
                                                 definition=service_definitions[service_code]))
        response.headers['Content-Type'] = 'text/xml; charset=utf-8'
        return response
    else:
        abort(404)


@app.route('/requests', methods=['GET', 'POST'])
def requests():
    ##Create and Submit Requests
    form = RequestForm()

    if request.method == 'POST':
        ## If the form is not valid, then load the request template.
        if form.validate() == False:
            return render_template('request.html', form=form)
        else:
            ##get data from the form, hardcoded some fill-ins.
            newRequest = serviceRequest(form.address.data, form.zipcode.data, form.service_code.data, 
                form.service_name.data, random.randint(100, 150), form.description.data, "Open", "N/A",
                form.request_date.data, "December 14th, 2016", "December 31, 2016", "Union College")
            db.session.add(newRequest) ##Add it to the database
            db.session.commit()
            return "Request Submitted!" ##Change to suitable page.
    elif request.method == 'GET':
        return render_template('request.html', form=form)

@app.route("/usersignup", methods=['GET', 'POST'])
def usersignup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('usersignup.html', form=form)
        else:
            newuser = Users(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            return "User SignUp Success!" ##Change to more suitable page
    elif request.method == 'GET':
        return render_template('usersignup.html', form=form)

@app.route("/adminsignup", methods=['GET', 'POST'])
def adminsignup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('adminsignup.html', form=form)
        else:
            newadmin = Admin(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newadmin)
            db.session.commit()

            return "Admin SignUp Success!" ##Change to more suitable page
    elif request.method == 'GET':
        return render_template('adminsignup.html', form=form)

@app.route("/usersignin", methods=["GET", "POST"])
def signin():

    form = SignInForm()

    if request.method == "POST":
        if form.validate() == False:
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = Users.query.filter_by(email=email).first()

            if user is not None and user.check_password(password):
                return "Login Success!!"
            else:
                return redirect(url_for('signin'))
    elif request.method == "GET":
        return render_template('login.html', form=form)

@app.route('/requests/<service_request_id>.<format>')
def service_request(service_request_id, format):
    """Query the current status of an individual request."""
    result = search(request.form)
    if format == 'json':
        return jsonify(srs[0])
    elif format == 'xml':
        response = make_response(render_template('service-requests.xml', service_requests=[srs[0]]))
        response.headers['Content-Type'] = 'text/xml; charset=utf-8'
        return response
    else:
        abort(404)


@app.route('/tokens/<token>.<format>')
def token(token, format):
    """Get a service request id from a temporary token. This is unnecessary
    if the response from creating a service request does not contain a token.
    """
    abort(404)


def search(service_request):
    """Query service requests"""
    pass # Implementation specific


def save(service_request):
    """Save service request"""
    # Implementation specific.  Just return a random SR id for now
    return {'service_request_id':random.randint(1,10000)}


if __name__ == '__main__':
    app.run()
