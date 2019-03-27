# -*- coding: utf-8 -*-

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .models import db, User


# creates a Blueprint named 'auth'
# The url_prefix will be prepended to all the URLs associated with the blueprint.
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'  # missing arguments
        elif not password:
            error = 'Password is required.'  # missing arguments
        elif User.query.filter_by(username=username).first() is not None:
            error = "username {} is already registered".format(username)  # existing user

        if error is None:
            user = User(username=username)
            user.hash_password(password)
            print("adding new user %s " % user)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        error = None
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None:
            error = 'Incorrect username.'
        elif not user.verify_password(request.form['password']):
            error = 'Incorrect password.'
        else:  # login succeed
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        # login fails
        flash(error)

    return render_template('auth/login.html')


# bp.before_app_request() registers a function that runs before the view
# function, no matter what URL is requested.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# This decorator returns a new view function that wraps the original view it’s
# applied to. The new function checks if a user is loaded and redirects to the
# login page otherwise. If a user is loaded the original view is called and
# continues normally.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:  # user not loaded
            return redirect(url_for('auth.login'))
        else:
            return view(**kwargs)
    return wrapped_view


