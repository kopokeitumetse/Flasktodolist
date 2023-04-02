from flask import Blueprint, render_template, request , flash, redirect, url_for

from . import db
from .model import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required,logout_user,current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods =['GET','POST'])
def login():
    if request.method == 'POST':
        email =request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(email = email).first()
        
        if user:
            if check_password_hash(user.password, password):
                print('loggesed in successlly')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))   
            else:
                print('No matching password')
        else:
            print('User does not exist')
            
    return render_template('login.html', user= current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods =['GET','POST'])
def sign_up():
    if request.method=="POST":
        username =request.form.get('username')
        password1=request.form.get('password1')
        password2= request.form.get('password2')
        first_name=request.form.get('fullName')


        user =User.query.filter_by(email=username).first()
        if user:
            flash('email already exist')
        elif len(username)< 4 :
            flash("Email must be creater than 4 charators")
        elif password1 !=  password2:
            flash("password does not match")
        elif len(password1)< 7:
            flash("password too short")
        else:
            new_user = User(email=username,first_name=first_name, password= generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            print('logged')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))    
    return render_template('sign_up.html', user= current_user)