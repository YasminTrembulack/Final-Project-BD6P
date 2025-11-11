import bcrypt

from flask import Flask, flash, redirect, render_template, request, session, url_for

from loguru import logger
from models.user import User

def configure_routes(app: Flask):
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')

        try:
            email_username = request.form.get('email_username', '').strip()
            password = request.form.get('password', '')

            # --- validações básicas ---
            if not email_username or not password:
                flash('Preencha todos os campos.', 'warning')
                return render_template('login.html')

            # --- busca por email OU username ---
            user = (
                User.get_user_by_field('email', email_username)
                or User.get_user_by_field('username', email_username)
            )

            # --- valida senha ---
            if not user:
                flash('Credenciais incorretas.', 'error')
                return render_template('login.html')

            hashed_password = user.password.encode('utf-8')
            input_password = password.encode('utf-8')

            if not bcrypt.checkpw(input_password, hashed_password):
                flash('Credenciais incorretas.', 'error')
                return render_template('login.html')

            # --- autenticação bem-sucedida ---
            session['user'] = {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                # "email": user.email,
                # "created_at": user.created_at,
            }

            session.permanent = True

            flash(f'Bem-vindo(a), {user.username}!', 'success')
            return redirect(url_for('get_books'))

        except Exception as e:
            logger.exception(f'Erro ao fazer login: {e}')
            flash('Erro inesperado ao tentar fazer login.', 'error')
            return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(request.referrer or url_for('index'))