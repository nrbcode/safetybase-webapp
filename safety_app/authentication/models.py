# -*- encoding: utf-8 -*-
# extensions
from flask_login import UserMixin
from flask_mongoengine import MongoEngine

import hashlib

# creations
db = MongoEngine()


class UserPreferences(db.EmbeddedDocument):

    """ Preferences """
    trim_tasks = db.BooleanField(default=False)
    prestart_pages = db.IntField(default=2)

    def to_json(self):

        return {
            "trim_tasks": self.trim_tasks,
            "prestart_pages": self.prestart_pages
        }

class User(db.Document, UserMixin):
    """ Create user. """
    username = db.StringField(required=True, max_length=50)
    email = db.EmailField(required=True)
    password = db.StringField(required=True)

    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    mobile = db.IntField()

    preferences = db.EmbeddedDocumentField(UserPreferences)
    
    def __str__(self):
        return f"User('{self.username}', '{self.email}')"

    def to_json(self):
        return {
            "username": self.username,
            "email": self.email
        }

    def avatar(self, size=300):
        # Encode the email to lowercase and then to bytes
        email_encoded = self.email.lower().encode('utf-8')

        # Generate the SHA256 hash of the email
        digest = hashlib.sha256(email_encoded).hexdigest()
        
        # construct url
        identicon_url = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest,
            size
        )

        return identicon_url


