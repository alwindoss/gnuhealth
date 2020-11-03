##############################################################################
#
#    Thalamus, the GNU Health Message and Authentication Server
#
#           Thalamus is part of the GNU Health project
#
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2019 Luis Falcon <falcon@gnuhealth.org>
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
from flask import Flask, g
from flask_login import current_user, LoginManager, login_required
from server.common.extensions import tryton, login_manager, Api

from server.common.utils import recordConverter
#from server.config import ProductionConfig
#from flask_tryton import Tryton

def before_request():
    """Allows access to user object
        for every request
    """
    g.user = current_user

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object('config.DebugConfig')
    if config is not None:
        app.config.from_object(config)
    app.config.from_envvar('FHIR_SERVER_CONFIG', silent=True)

    with app.app_context():
        import logging
        logging.basicConfig(filename='flask.log', level=logging.INFO,
                format='%(asctime)s:::%(levelname)s:::%(name)s: %(message)s')

        # Initialize tryton
        tryton.init_app(app)

        # Login
        login_manager.init_app(app)
        login_manager.login_view='auth_endpoint.login'
        login_manager.session_protection='strong'

        # Initiate the REST API
        api=Api(app)

        # The user model
        user = tryton.pool.get('res.user')

        # Setup tryton config
        @tryton.default_context
        def default_context():
            return user.get_preferences(context_only=True)

        # Add Model-ID-Field url converter
        app.url_map.converters['item']=recordConverter

        # Store current user in g.user
        app.before_request(before_request)

        #### ADD THE ROUTES ####
        from resources.system import Conformance
        api.add_resource(Conformance, '/', '/metadata')

        def add_fhir_routes(resource):
            """Adds complex FHIR routes"""

            for _, route in resource.routing_table.items():
                api.add_resource(route['handler'], *route['uri'])

        from resources.patient import routing as pat
        add_fhir_routes(pat)

        from resources.diagnostic_report import routing as dr
        add_fhir_routes(dr)

        from resources.observation import routing as obs
        add_fhir_routes(obs)

        from resources.practitioner import routing as hp
        add_fhir_routes(hp)

        from resources.procedure import routing as op
        add_fhir_routes(op)

        from resources.condition import routing as condition
        add_fhir_routes(condition)

        from resources.family_history import routing as fh
        add_fhir_routes(fh)

        from resources.medication import routing as med
        add_fhir_routes(med)

        from resources.medication_statement import routing as ms
        add_fhir_routes(ms)

        from resources.immunization import routing as imm
        add_fhir_routes(imm)

        from resources.organization import routing as org
        add_fhir_routes(org)

        # Handle the authentication blueprint
        #   TODO: Use OAuth or something robust
        from resources.auth import auth_endpoint
        app.register_blueprint(auth_endpoint, url_prefix='/auth')

    return app

if __name__=="__main__":
    create_app().run(debug=True)
