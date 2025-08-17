# -*- encoding: utf-8 -*-
"""
Authentication module initialization routine
"""

from flask import Blueprint

blueprint = Blueprint('authentication_blueprint', __name__, url_prefix='')

