# -*- encoding: utf-8 -*-
"""
This may not be needed with flask-mongoengine
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.simple import TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email, DataRequired

#from ..authentication.models import db, User

class ChecklistForm(FlaskForm):

    site = StringField("Site", validators=[InputRequired()])
    activity = StringField("Activity")
    comment = TextAreaField("Comment", validators=[InputRequired()])

    submit = SubmitField("Post Entry")
