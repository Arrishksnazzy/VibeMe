from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import RegistrationForm, LoginForm, MoodForm
from app.models import User, MoodEntry
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Создаем нового пользователя
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # Сохраняем в базу данных
        db.session.add(user)
        db.session.commit()
        
        flash('🎉 Регистрация прошла успешно! Теперь вы можете войти в систему.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Ищем пользователя по email
        user = User.query.filter_by(email=form.email.data).first()
        
        # Проверяем пароль
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash(f'🌈 Добро пожаловать, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('❌ Неверный email или пароль. Попробуйте еще раз.', 'danger')
    
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('👋 Вы вышли из системы. Возвращайтесь скорее!', 'info')
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    # Получаем последние записи настроения пользователя
    recent_moods = MoodEntry.query.filter_by(user_id=current_user.id)\
                                 .order_by(MoodEntry.timestamp.desc())\
                                 .limit(5).all()
    return render_template('dashboard.html', recent_moods=recent_moods)

@bp.route('/mood', methods=['GET', 'POST'])
@login_required
def mood_form():
    form = MoodForm()
    if form.validate_on_submit():
        # Создаем новую запись настроения
        mood_entry = MoodEntry(
            mood=form.mood.data,
            notes=form.notes.data,
            author=current_user
        )
        
        # Сохраняем в базу данных
        db.session.add(mood_entry)
        db.session.commit()
        
        flash('✅ Настроение успешно сохранено!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('mood_form.html', form=form)

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)