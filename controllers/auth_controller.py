from flask import Flask, flash, redirect, render_template, request, session, url_for
from models.user import User

def configure_routes(app: Flask):
    
    @app.route('/login', method=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            user = User.get_by_email(email)
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['user_role'] = user.role
                session['user_email'] = user.email
                session['user_username'] = user.username
                session['user_created_at'] = user.created_at
                return redirect(url_for('books'))
            else:
                flash('Email ou senha incorretos!')

        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        session.clear()  # limpa todos os dados da sessão
        return redirect(url_for('login'))
