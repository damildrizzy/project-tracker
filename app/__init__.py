import os

from flask import Flask
#from flask_assets import Environment
from flask_compress import Compress
from flask_login import LoginManager
from flask_mail import Mail
from flask_rq import RQ
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_restful import Api

#from app.assets import app_css, app_js, vendor_css, vendor_js
from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()
csrf = CSRFProtect()
compress = Compress()
marshmallow = Marshmallow()
jwt = JWTManager()


# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    

    config[config_name].init_app(app)

    # Set up extensions
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    #csrf.init_app(app)
    compress.init_app(app)
    RQ(app)
    jwt.init_app(app)
    marshmallow.init_app(app)
    api = Api(app)


    # # Set up asset pipeline
    # assets_env = Environment(app)
    # dirs = ['assets/styles', 'assets/scripts']
    # for path in dirs:
    #     assets_env.append_path(os.path.join(basedir, path))
    # assets_env.url_expire = True

    # assets_env.register('app_css', app_css)
    # assets_env.register('app_js', app_js)
    # assets_env.register('vendor_css', vendor_css)
    # assets_env.register('vendor_js', vendor_js)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Create app blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from app.api.auth import AuthView
    from app.api.v1.user import UserView
    from app.api.v1.project import ProjectView, ProjectsView,TicketView, TicketsView, CommentView


    api.add_resource(AuthView, '/api/auth')
    api.add_resource(UserView, '/api/v1/users')
    api.add_resource(ProjectsView, '/api/v1/projects')
    api.add_resource(ProjectView, '/api/v1/project/<int:id>')
    api.add_resource(TicketView, '/api/v1/project/<int:id>/tickets')
    api.add_resource(TicketView, '/api/v1/project/<int:id>/tickets/<int:tid>', endpoint="ticket")
    api.add_resource(TicketsView, '/api/v1/tickets')
    api.add_resource(CommentView, '/api/v1/project/<int:id>/tickets/<int:tid>/comment')

    
    return app
