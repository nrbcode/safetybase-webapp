# -*- encoding: utf-8 -*-
"""
The flask application package.
"""

# libraries
from importlib import import_module
from flask import Flask

# modules
from .authentication.routes import bc, login_manager
from .authentication.models import db

def register_extensions(app):

    # Initialize extensions
    login_manager.init_app(app)
    bc.init_app(app)
    db.init_app(app)
    print("Extensions registered.")

def register_blueprints(app):

    # Register blueprints on the app
    for module_name in ('authentication', 'home'):
        module = import_module('safety_app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)
    print("Blueprints registered")

def create_app(conf_object: str=None):

    # app factory
    app = Flask(__name__)
    
    app.config.from_object(conf_object)
    print(f"Configured with db: {app.config.get('MONGODB_SETTINGS')['db']}")
    
    register_extensions(app)
    register_blueprints(app)
    
    return app

