from flask import Blueprint, render_template, url_for, redirect, current_app
from app.models import AdminUser, Book
from app.db import get_db
from flask_admin import Admin
from flask_login import login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_admin.contrib.sqla import ModelView
import bcrypt

bp = Blueprint('admins', __name__, url_prefix='/admins')
salt = bcrypt.gensalt()
    
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        db = get_db()
        existing_admin_username = db.query(AdminUser).filter_by(username = username).first()

        if existing_admin_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")


@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db = get_db();
        user = db.query(AdminUser).filter_by(username=form.username.data).first()
        if user:
            if bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
                login_user(user)
                return redirect(url_for('admin.index'))
        else:
            return redirect (url_for('incorrect'))
            return render_template ('incorrect.html')
    return render_template('login.html', form = form)

@bp.route('/incorrect', methods = ['GET', 'POST'])
def incorrect():
    return render_template ('incorrect.html')

@bp.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        db = get_db();
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
        print(hashed_password)
        new_admin = AdminUser(username=form.username.data, password=hashed_password)
        db.add(new_admin)
        db.commit()
        return redirect(url_for('admins.login'))

    return render_template('register.html', form = form)

@bp.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('dashboard.html')