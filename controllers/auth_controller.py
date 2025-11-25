import bcrypt

from flask_mail import Mail, Message
from flask import Flask, flash, redirect, render_template, request, session, url_for

from loguru import logger
from models.user import User

from itsdangerous import URLSafeTimedSerializer


def configure_routes(app: Flask):

    mail = Mail(app)
    serializer = URLSafeTimedSerializer(app.secret_key)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')

        try:
            email_username = request.form.get('email_username', '').strip()
            password = request.form.get('password', '')

            if not email_username or not password:
                flash('Preencha todos os campos.', 'warning')
                return render_template('login.html')

            user = (
                User.get_user_by_field('email', email_username)
                or User.get_user_by_field('username', email_username)
            )

            if not user:
                flash('Credenciais incorretas.', 'error')
                return render_template('login.html')

            hashed_password = user.password.encode('utf-8')
            input_password = password.encode('utf-8')

            if not bcrypt.checkpw(input_password, hashed_password):
                flash('Credenciais incorretas.', 'error')
                return render_template('login.html')

            session['user'] = {
                "id": user.id,
                "username": user.username,
                "role": user.role,
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


    @app.route('/forgot_password', methods=['GET', 'POST'])
    def forgot_password():
        if request.method == 'POST':
            email = request.form.get('email')
            user = User.get_user_by_field('email', email)

            if not user:
                flash("Email não vinculado a nenhuma conta. Por favor, digite um email válido.", "info")
                return redirect(url_for('forgot_password'))

            token = serializer.dumps(user.email, salt='password-reset-salt')

            reset_url = url_for('reset_password', token=token, _external=True)

            html = render_template(
                'reset-password-email.html',
                reset_url=reset_url,
                user_name=user.username,
                year=2025
            )

            msg = Message(
                subject="Recuperação de senha - LitScore",
                recipients=[user.email],
                body=f"Redefinição de senha\n\nAcesse: {reset_url}\n\nSe você não solicitou, ignore.",
                html=html,
                sender=app.config['MAIL_USERNAME']
            )

            mail.send(msg)

            flash("Se o e-mail existir, você receberá um link para redefinir sua senha.", "info")
            return redirect(url_for('login'))

        return render_template('password.html', forgot_password=True)


    @app.route('/reset_password/<token>', methods=['GET', 'POST'])
    def reset_password(token):
        try:
            email = serializer.loads(token, salt='password-reset-salt', max_age=600)
        except Exception:
            flash("Link inválido ou expirado.", "error")
            return redirect(url_for('forgot_password'))

        if request.method == 'POST':
            password = request.form.get('password')
            confirm = request.form.get('confirm-password')

            if password != confirm:
                flash("As senhas não coincidem.", "warning")
                return redirect(url_for('reset_password', token=token))

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = User.get_user_by_field('email', email)
            user.password = hashed_password
            User.update_user(user)

            flash("Senha atualizada com sucesso!", "success")
            return redirect(url_for('login'))

        return render_template('password.html', token=token)
