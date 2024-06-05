from flask import render_template, redirect, request, url_for, flash
from app.domain.models import User
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash


def user_routes(app, db, login_manager):
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.pasword_hash, password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Invalid email or password')
            
        return render_template('login.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            
            if not username or not email or not password:
                flash('please fill all the fields')
                redirect(url_for('register'))
            
            user = User.query.filter_by(email=email).first()
            if user:
                flash('user email already exists')
                return redirect(url_for('register'))
            
            user = User(username=username, email=email)
            user.set_password(password=password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('registration successful')
            return redirect(url_for('login'))
            
        return render_template('register.html')
    
    @app.route('/')
    @login_required
    def home():
        return render_template('home.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
        
        