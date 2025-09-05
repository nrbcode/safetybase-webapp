# -*- encoding: utf-8 -*-
"""
Configuration objects for various environments.
"""
from os import environ
from datetime import timedelta

from dotenv import load_dotenv

class Config():
	load_dotenv()

	CSRF_ENABLED			 = True
	REMEMBER_COOKIE_DURATION = timedelta(days=1)
	SECRET_KEY				 = environ.get('SECRET_KEY')

class ConfigRemoteDev(Config):

	"""configurations for development with atlas."""
	MONGODB_SETTINGS		= {
		'db': 'remote-safetybase',
		'host': environ.get('ATLAS_URI')
	}
	
class ConfigLocalDev(Config):

	"""configurations for local development"""
	MONGODB_SETTINGS = {
		'db': 'safetybase',
		'host': 'localhost',
		'port': 27017
	}

