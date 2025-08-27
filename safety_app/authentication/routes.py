# -*- encoding: utf-8 -*-
'''
Authentication routes and views

next_page = request.args.get('next')
if not next_page or url_parse(next_page).netloc != '':
    next_page = url_for('home_blueprint.index')
'''

# libraries
#import json
from datetime import datetime
from flask import render_template, redirect, request, url_for, session, jsonify

# extensions
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt

# modules
from safety_app.authentication import blueprint
from safety_app.authentication.forms import LoginForm, CreateAccountForm
from safety_app.authentication.models import User, UserPreferences

# creations
bc = Bcrypt()
login_manager = LoginManager()

# initial endpoint
login_manager.login_view = 'authentication_blueprint.route_default'

# user callback
@login_manager.user_loader
def load_user(user_id):
    return User.objects(email=user_id).first()

# request callback
@login_manager.request_loader
def request_loader(request):
    name = request.form.get('username')
    user = User.objects(username=name).first()
    
    return user if user else None

# Views

@blueprint.route('/')
def route_default():

    #return redirect(url_for('home_blueprint.index'))
    return render_template('home/index.html', title='Home Page', year=datetime.now().year)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    msg = None

    # check if both http method is POST and form is valid on submit
    if login_form.validate_on_submit():

        # assign form data to variables
        username = login_form.username.data
        password = login_form.password.data
        
        # filter user from users
        user = User.objects(username=username).first()
        
        if user:
           if bc.check_password_hash(user.password, password):

               # set flask-login properties
               user.id = user.email
               user.username = username
               login_user(user)
               #login_user(user, remember=login_form.remember_me.data)
               session['name'] = username

               #return jsonify(user.to_json())
               #return redirect(url_for('home_blueprint.dashboard'))
               return redirect(url_for('home_blueprint.index'))
               
           else:
               msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"

    return render_template('account/login.html', form=login_form, msg=msg)

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    msg = None
    
    # check if http method is POST and form is valid on submit
    if create_account_form.validate_on_submit():
        
        username = create_account_form.username.data
        email = create_account_form.email.data
        password = create_account_form.password.data        
        default_preferences = UserPreferences()

        user_by_name = User.objects(username=username).first()
        user_by_email = User.objects(email=email).first()

        if user_by_name or user_by_email:
            msg = 'Error: User exists!'
            print(msg)
            return render_template('account/register.html', msg=msg, success=False, form=create_account_form)
        
        else:
            pw_hash = bc.generate_password_hash(password)
            User(username=username, email=email, password=pw_hash, preferences=default_preferences).save()
            msg = 'User created, please <a href="' + url_for('.login') + '">login</a>'
            print(msg)
            
    return render_template('account/register.html', msg=msg, success=True, form=create_account_form)

@blueprint.route('/logout')
@login_required
def logout():
    if session.get('name'):
        session.pop('name')
    logout_user()
    
    #return redirect(url_for('authentication_blueprint.login'))
    return render_template('home/index.html')

@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    if request.method == 'POST':
        current_user.update(**request.form)

        # display updated profile by redirection
        return redirect(url_for('.user_profile'))

    return render_template('account/profile.html')

@blueprint.route('/user_info', methods=['GET'])
@login_required
def user_info():
    if current_user.is_authenticated:
        resp = {"result": 200,
                "data": current_user.to_json()}
    else:
        resp = {"result": 401,
                "data": {"message": "user no login"}}
    return jsonify(**resp)

@blueprint.route('/account')
@login_required
def account():
    return render_template('account/account.html')

@blueprint.route('/session')
@login_required
def session_example():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return f'Visits: {session.get("visits")}'


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():

    return render_template('home/page-403.html'), 403
    #return render_template('home/index.html')


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
