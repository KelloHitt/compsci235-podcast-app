from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from password_validator import PasswordValidator
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import podcast.adapters.repository as repo
import podcast.authentication.services as services
import podcast.utilities.utilities as utilities

# Configure Blueprint.
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_error = None
    password_error = None

    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            services.add_user(form.username.data, form.password.data, repo.repo_instance)
            flash("Registration successful!", "success")
            # All is well, redirect the user to the login page.
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            username_error = "Your username is already taken - please try another one."

    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'authentication/credentials.html',
        title='Register',
        form=form,
        username_error=username_error,
        password_error=password_error,
        categories=utilities.get_categories()['categories']
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_error = None
    password_error = None

    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to look up the user.
        try:
            user = services.get_user(form.username.data, repo.repo_instance)

            # Authenticate user.
            services.authenticate_user(user['username'], form.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['username'] = user['username']
            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            # Username not known to the system, set a suitable error message.
            username_error = "This username is not registered!"

        except services.AuthenticationException:
            # Authentication failed, set a suitable error message.
            password_error = "Password and username do not match - please check and try again!"

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'authentication/credentials.html',
        title='Login',
        username_error=username_error,
        password_error=password_error,
        form=form,
        categories=utilities.get_categories()['categories']
    )


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)

    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = "Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit."
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema.min(8).has().uppercase().has().lowercase().has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField("Username", [
        DataRequired(message="Your username is required"),
        Length(min=3, message="Your username is too short")],
                           render_kw={"placeholder": "Username"})
    password = PasswordField("Password", [
        DataRequired(message="Your password is required"),
        PasswordValid()],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", [DataRequired(message="Your username is required")],
                           render_kw={"placeholder": "Username"})
    password = PasswordField("Password", [DataRequired(message="Your password is required")],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")
