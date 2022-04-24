from flask import Blueprint, render_template, request, redirect, url_for, flash
from marvel_project.models import User, db, check_password_hash
from marvel_project.forms import UserLoginForm, UserSignUpForm

#Imports for Flask Login
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder= 'auth_templates')

@auth.route('/signup', methods = ['POST', 'GET'])
def signup():
    form = UserSignUpForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            password = form.password.data
            print(username, password)

            user = User(first_name=first_name, last_name=last_name, username=username, password=password)

            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a user account: {username}", 'user-created')

            return redirect(url_for('site.home'))

    except:
        raise Exception('Invalid Form Data: Please Check Your Form')    
    
    return render_template('signup.html', form=form)

@auth.route('/signin', methods = ['POST', 'GET'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            print(username, password)

            logged_user = User.query.filter(User.username == username).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in: Via username/password', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your username/pasword is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    return render_template('signin.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))