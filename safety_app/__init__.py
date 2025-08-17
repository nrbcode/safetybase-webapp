# -*- encoding: utf-8 -*-
"""
The flask application package.
"""
from flask import Flask


def create_app(conf_object: str=None):

    # app factory
    app = Flask(__name__)
    app.config.from_object(conf_object)

    return app

