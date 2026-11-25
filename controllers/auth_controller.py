import os
import bcrypt

from flask_mail import Mail, Message
from flask import Flask, flash, redirect, render_template, request, session, url_for

from loguru import logger
from models.user import User

from itsdangerous import URLSafeTimedSerializer

BASE_URL = os.getenv('APP_BASE_URL', 'http://127.0.0.1:5000').rstrip('/')

def configure_routes(app: Flask):
    """
    Configura todas as rotas relacionadas à autenticação e recuperação de senha.
    """


    # ==========================================================
    # 📬 Configuração do serviço de e-mail
    # ==========================================================
    mail = Mail(app)


    # ==========================================================
    # 🔑 Gerador de tokens seguros
    # ==========================================================
    # O serializer utiliza a SECRET_KEY do app para gerar tokens únicos e seguros,
    # usados para recuperação de senha (com validade configurável em segundos).
    serializer = URLSafeTimedSerializer(app.secret_key)


    # ==========================================================
    # 🔐 LOGIN - Página e autenticação de usuários
    # ==========================================================
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
            }

            session.permanent = True

            flash(f'Bem-vindo(a), {user.username}!', 'success')
            return redirect(url_for('get_books'))

        except Exception as e:
            logger.exception(f'Erro ao fazer login: {e}')
            flash('Erro inesperado ao tentar fazer login.', 'error')
            return render_template('login.html')


    # ==========================================================
    # 🚪 LOGOUT - Finaliza sessão e redireciona
    # ==========================================================
    @app.route('/logout')
    def logout():
        """Finaliza a sessão atual e retorna à página anterior ou inicial."""
        session.clear()
        return redirect(url_for('index'))


    # ==========================================================
    # 🔄 RECUPERAÇÃO DE SENHA - Etapa 1: Solicitação de redefinição
    # ==========================================================
    @app.route('/forgot_password', methods=['GET', 'POST'])
    def forgot_password():
        """
        Página de recuperação de senha:
        - Recebe o e-mail do usuário
        - Gera token temporário
        - Envia link de redefinição por e-mail
        """
        if request.method == 'POST':
            email = request.form.get('email')
            user = User.get_user_by_field('email', email)

            # --- Validação: e-mail inexistente ---
            if not user:
                flash("Email não vinculado a nenhuma conta. Por favor, digite um email válido.", "info")
                return redirect(url_for('forgot_password'))

            # --- Criação do token seguro para redefinição ---
            token = serializer.dumps(user.email, salt='password-reset-salt')

            # --- Gera o link de redefinição completo ---
            reset_url = f"{BASE_URL}{url_for('reset_password', token=token)}"

            # --- Gera o conteúdo HTML do e-mail ---
            html = render_template(
                'reset-password-email.html',
                reset_url=reset_url,
                user_name=user.username,
                year=2025
            )

            # ==========================================================
            # 📧 Envio do e-mail de recuperação (via Mailtrap: https://mailtrap.io/home)
            # ==========================================================
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

        # --- Exibe o formulário de recuperação ---
        return render_template('password.html', forgot_password=True)


    # ==========================================================
    # 🔑 REDEFINIÇÃO DE SENHA - Etapa 2: Novo cadastro de senha
    # ==========================================================
    @app.route('/reset_password/<token>', methods=['GET', 'POST'])
    def reset_password(token):
        """
        Página de redefinição de senha:
        - Valida o token
        - Permite atualizar a senha
        """
        try:
            # Valida e decodifica o token (expira em 10 minutos = 600s)
            email = serializer.loads(token, salt='password-reset-salt', max_age=600)
        except Exception:
            flash("Link inválido ou expirado.", "error")
            return redirect(url_for('forgot_password'))

        if request.method == 'POST':
            password = request.form.get('password')
            confirm = request.form.get('confirm-password')

            # --- Verifica correspondência das senhas ---
            if password != confirm:
                flash("As senhas não coincidem.", "warning")
                return redirect(url_for('reset_password', token=token))

            # --- Atualiza senha no banco (com hash seguro) ---
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = User.get_user_by_field('email', email)
            user.password = hashed_password
            User.update_user(user)

            flash("Senha atualizada com sucesso!", "success")
            return redirect(url_for('login'))

        # --- Exibe o formulário para redefinir senha ---
        return render_template('password.html', token=token)
