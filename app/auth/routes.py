from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User, db
import re

auth_bp = Blueprint('auth', __name__)

# WTForms для валидации
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    name = StringField('Полное имя', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    company = StringField('Компания', validators=[Length(max=200)])
    position = StringField('Должность', validators=[Length(max=100)])
    phone = StringField('Телефон', validators=[Length(max=20)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Подтвердите пароль', 
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Пользователь с таким email уже зарегистрирован.')

    def validate_password(self, password):
        # Проверка сложности пароля
        if not re.search(r'[A-Za-z]', password.data):
            raise ValidationError('Пароль должен содержать буквы.')
        if not re.search(r'[0-9]', password.data):
            raise ValidationError('Пароль должен содержать цифры.')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.update_last_login()
            
            # Перенаправление на изначально запрошенную страницу
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('dashboard')
            
            flash('Добро пожаловать!', 'success')
            return redirect(next_page)
        else:
            flash('Неверный email или пароль', 'error')
    
    return render_template('auth/login.html', title='Вход', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data.strip(),
            email=form.email.data.lower().strip(),
            company=form.company.data.strip() if form.company.data else None,
            position=form.position.data.strip() if form.position.data else None,
            phone=form.phone.data.strip() if form.phone.data else None
        )
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Регистрация успешна! Теперь вы можете войти в систему.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {e}")
            flash('Ошибка при регистрации. Попробуйте еще раз.', 'error')
    
    return render_template('auth/register.html', title='Регистрация', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'info')
    return redirect(url_for('landing'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)
