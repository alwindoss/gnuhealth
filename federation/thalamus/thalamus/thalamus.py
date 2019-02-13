# -*- coding: utf-8 -*-
##############################################################################
#
#    Thalamus, the GNU Health Message and Authentication Server
#
#           Thalamus is part of the GNU Health project
#
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2019 Luis Falcon <lfalcon@gnusolidario.org>
#    Copyright (C) 2011-2019 GNU Solidario <health@gnusolidario.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from flask import Flask, redirect, request, jsonify, render_template, url_for
from flask_restful import Resource, Api, abort

import psycopg2

from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, \
    validators

from flask_httpauth import HTTPBasicAuth
import json
import bcrypt
import logging

__all__ = ["People","Person","Book","Page", "PasswordForm","Password"]

app = Flask(__name__)
app.config.from_pyfile('etc/thalamus.cfg')

api = Api(app)

auth = HTTPBasicAuth()

ACL = json.load(open(app.config['ACL'],'r'))

# Use Gunicorn logging system when Thalamus is run through it
# use the gunicorn argument --log-level to specify the starting
# level of the application (eg, --log-level=debug)
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


#Open a connection to PG Server
conn = psycopg2.connect(app.config['POSTGRESQL_URI'])

def check_person(person_id):
    """
    Checks if the Federation ID exists on the GNU Health HIS
    Returns the instance or null
    """
    cur = conn.cursor()
    cur.execute ('SELECT id from people \
        where id = %s limit(1)', (person_id,))
    try:
        person, = cur.fetchone()
    except:
        person = None

    return person

# Authentication

@auth.verify_password
def verify_password(username, password):
    """
    Takes the username and password from the client
    and checks them against the entry on the people db collection
    The password is bcrypt hashed
    """
    cur = conn.cursor()
    cur.execute ('SELECT data from people \
        where id = %s limit(1)', (username,))
    try:
        user, = cur.fetchone()
    except:
        user = None

    if (user):
        person = user['id']
        hashed_password = user['password']
        roles = user['roles']
        if bcrypt.checkpw(password.encode('utf-8'),
            hashed_password.encode('utf-8')):
            """ Authentication OK
            Now check the access level for the resource
            """
            method = request.method
            endpoint = request.endpoint
            view_args = request.view_args
            return access_control(username,roles, method, endpoint, view_args)

        else:
            return False

    else:
       return False



# Authorization
def access_control(username, roles, method, endpoint, view_args):
    """
    Takes the logged in user roles, method and endpoint as arguments
    Verifies them against the ACL and returns either True or False
    """    
    for user_role in roles:
        for acl_entry in ACL:
            if (acl_entry["role"] == user_role):
                actions = acl_entry["permissions"]
                if (endpoint in actions[method]):
                    """Check if the method allows to access the endpoint"""
                    if view_args:
                        """If there are arguments (eg, person_id), check
                            whether the user role has global access
                            or just can see his/her records"""
                        if (username == view_args["person_id"] or
                            actions["global"] == "True"):
                                return True
                    else:
                        return True
    return False

# People Resource
class People(Resource):
    """Collection resource for demographic information"""

    decorators = [auth.login_required] # Use the decorator from httpauth
    def get(self):
        """
        Retrieves all the people on the person collection
        """
        cur = conn.cursor()
        cur.execute ('SELECT data from people')
        people = cur.fetchall()

        return jsonify(people)

# Person
class Person(Resource):
    """Class that manages the person demographics.
    """

    decorators = [auth.login_required] # Use the decorator from httpauth

    def get(self, person_id):
        """
        Retrieves the person instance
        """
        cur = conn.cursor()
        cur.execute ('SELECT data from people \
            where id = %s limit(1)', (person_id,))

        try:
            person, = cur.fetchone()
        except:
            person = None

        # Return a 404 if the person ID is not found
        if not person:
            return '', 404

        return jsonify(person)

    def post(self, person_id):
        """
        Create a new instance on the Person resource
        Initially just the Federation ID and the bcrypted
        hashed password
        """

        #Grab the data coming from the client, in JSON format
        values = json.loads(request.data)

        # Initialize to inactive the newly created person
        values['active'] = False
        pw = None

        bcrypt_prefixes = ["$2b$", "$2y$"]

        if check_person(person_id):
            abort (422, error="User already exists")

        if (person_id):
            if (type(person_id) is str):
                #Use upper case on the person federation account
                values['id'] = person_id.upper()
        else:
            abort (422, error="wrong format on person ID")

        #If no roles are supplied, assign "end_user"
        if not ('roles' in values.keys()):
            values['roles'] = ["end_user"]


        if ('password' in values.keys()):
            pw = values['password']

        if (pw):
            if (len(pw) > 64):
                abort (422, error="Password is too long")

            # Check if the password is already in bcrypt format
            if (pw[0:4] in bcrypt_prefixes):
                hashed_pw = pw
            else:
                hashed_pw = (bcrypt.hashpw(pw.encode('utf-8'),
                    bcrypt.gensalt())).decode('utf-8')

            values['password'] = hashed_pw

        # Insert the newly created person
        cur = conn.cursor()
        cur.execute("INSERT INTO people (ID, DATA) VALUES (%(id)s, \
            %(data)s)", {'id': person_id, 'data':json.dumps(values)})
        res = conn.commit()

        return jsonify(res)


    def patch(self, person_id):
        """
        Updates the person instance
        """

        #Grab all the data coming from the node client, in JSON format
        values = json.loads(request.data)

        if 'id' in values:
            # Avoid changing the user ID
            abort(422, error="Not allowed to change the person ID")
            # TO be discussed...
            # Check if the new ID exist in the Federation, and if it
            # does not, we may be able to update it.

        if check_person(person_id):
            update_person = db.people.update_one({"id":person_id},
                {"$set": values})
        else:
            abort (404, error="User not found")

    def delete(self, person_id):
        """
        Delete the user instance. This will be
        used in exceptional cases only, and the
        instance must be inactive.
        """
        person = check_person(person_id)
        if not person:
            abort (404, error="User does not exist")

        else:
           if person['active']:
            abort (422, error="The user is active.")

        delete_person = db.people.delete_one({"id":person_id})

# Book of Life Resource
class Book(Resource):
    """Collection resource for a person life information"""

    decorators = [auth.login_required] # Use the decorator from httpauth

    def get(self, person_id):
        """
        Retrieves the pages of life from the person
        """
        pages = list(db.pols.find({'book' : person_id}))

        # Return a 404 if the person ID is not found
        if not pages:
            return '', 404

        return jsonify(pages)


# Page of Life
class Page(Resource):
    """Information and events that make and shape a person life"""

    decorators = [auth.login_required] # Use the decorator from httpauth

    def get(self, person_id, page_id):
        """
        Retrieves the page instance
        """
        page = db.pols.find_one({'id': page_id})

        # Return a 404 if the person ID is not found
        if not page:
            abort (404, error="Book or page or not found")

        return jsonify(page)

    def post(self, person_id, page_id):
        """
        Create a new instance on the Page resource
        """
        #Grab the data coming from the client, in JSON format
        values = json.loads(request.data)

        # Basic validation on page ID exsistance and string type
        if (person_id and 'id' in values):
            if (type(person_id) is str and type(values['id'])):
                # Insert the newly created PoL in MongoDB
                page = db.pols.insert(values)
        else:
            print ("wrong format on person or page ID")
            abort (422, error="wrong format on person or page ID")

        return jsonify(page)

    def patch(self, person_id, page_id):
        """
        Updates the Page of Life
        """

        #Grab all the data coming from the node client, in JSON format
        values = json.loads(request.data)

        if 'id' in values:
            # Avoid changing the user ID
            abort(422, error="Not allowed to change the page ID")
            # TO be discussed...
            # Check if the new ID exist in the Federation, and if it
            # does not, we may be able to update it.

        if check_person(person_id):
            update_page = db.pols.update_one({"id":page_id},
                {"$set": values})
        else:
            abort (404, error="Page not found")

# Add resources and endpoints
# The endpoints are the class names in lower case (eg, people, life, page...)

#People and person
api.add_resource(People, '/people') #Add resource for People
api.add_resource(Person, '/people/<string:person_id>') #Add person instance

#Book and pages of life resources (in pols collection)
api.add_resource(Book, '/pols/<string:person_id>')
api.add_resource(Page, '/pols/<string:person_id>/<string:page_id>')

# Personal Documents resource
class PersonalDocs(Resource):
    "Documents associated to the person (scanned info, birth certs, ..)"
    def get(self):
        documents = list(db.personal_document.find())
        return jsonify(documents)

api.add_resource(PersonalDocs, '/personal-documents')

# Domiciliary Units resource
class DomiciliaryUnits(Resource):
    "Domiciliary Units"
    def get(self):
        dus = list(db.domiciliary_unit.find())
        return jsonify(dus)

api.add_resource(DomiciliaryUnits, '/domiciliary-units')


# Institutions resource
class Institutions(Resource):
    "Health and other institutions"

    decorators = [auth.login_required] # Use the decorator from httpauth

    def get(self):
        institutions = list(db.institution.find())
        return jsonify(institutions)

api.add_resource(Institutions, '/institutions')

class PasswordForm(FlaskForm):
    password = PasswordField('Password',
        validators=[validators.DataRequired(),
        validators.Length(min=6, max=30),
        validators.EqualTo('pconfirm', message='Password mistmatch')])
    pconfirm = PasswordField('Confirm Password')
    update = SubmitField('Update')
   

# Update the password of the user with a form
@app.route('/password/<person_id>', methods=('GET', 'POST'))
@auth.login_required
def password(person_id):
    error = None
    form = PasswordForm()
    if (request.method == 'POST' and form.validate()):
            pwd = form.password.data.encode()
            enc_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt()).decode()
            values = {'password': enc_pwd}
            update_password = \
                db.people.update_one({"id":person_id},{"$set": values})

            if update_password:
                return redirect(url_for('index'))
            else:
                error = "Error updating the password"
    return render_template('password.html', form=form, \
        fed_account=person_id, error=error)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.logger.warning("Running Thalamus without gunicorn ...")
    app.run()
