from datetime import datetime, timezone
import bcrypt

from loguru import logger

from flask import Flask, flash, redirect, render_template, request, session, url_for
from models.user import User, UserEntity

def configure_routes(app: Flask):

    # GET - retorna todos os usuários
    @app.route('/get_users', methods=['GET'])
    def get_users():
        per_page = 20
        page = int(request.args.get('page', 1)) if session.get('user') else 1
        users_response = User.get_users(page ,per_page)
        
        pagination = users_response['pagination'].to_dict()
        total_pages = pagination['total_pages']

        start_page = max(1, page - 2)
        end_page = min(total_pages, page + 2)
        
        users = users_response['data']

        return render_template(
            'users.html',
            empty_cards= (3 - (len(users) % 3)) % 3,
            logged_user=session.get('user'),
            pagination_info=pagination,
            start_page=start_page,
            end_page=end_page,
            users=users,
        )

    # GET - retorna um usuário por ID
    @app.route('/get_user/<user_id>', methods=['GET'])
    def get_user(user_id):
        return render_template('profile.html', logged_user=session.get('user'))

    # POST - cria um novo usuário
    @app.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'GET':
            return render_template('register.html')
        try:
            form = request.form
            username = form.get('username', '').strip()
            email = form.get('email', '').strip()
            password = form.get('password')
            confirm = form.get('confirm-password')
            role =  form.get('role') or 'user'

            # --- Validações ---
            if not username or not email or not password or not confirm:
                flash('Todos os campos são obrigatórios.', 'warning')
                return redirect(url_for('register'))

            if User.get_user_by_field('username', username):
                flash('Nome de usuário já utilizado, escolha outro.', 'warning')
                return redirect(url_for('register'))

            if User.get_user_by_field('email', email):
                flash('Email já cadastrado, tente fazer login.', 'warning')
                return redirect(url_for('register'))

            if password != confirm:
                flash('As senhas não coincidem.', 'warning')
                return redirect(url_for('register'))

            # --- Criação segura ---
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            new_user = UserEntity(
                username=username,
                email=email,
                password=hashed_password,
                role=role,
            )

            User.create_user(new_user)

            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            logger.exception(f'Erro ao cadastrar usuário: {e}')
            flash('Ocorreu um erro ao cadastrar o usuário.', 'error')
            return redirect(url_for('register'))


    # PUT - atualiza um usuário
    @app.route('/update_user/<user_id>', methods=['POST']) 
    def update_user(user_id):
        form = request.form
        username = form.get('username', '').strip()
        role = form.get('role', '')
        created_at = form.get('created_at', '')
        email = form.get('email', '').strip()
        password = form.get('password')
        confirm = form.get('confirm-password')
        
        if User.get_user_by_field('username', username):
            flash('Nome de usuário já utilizado, escolha outro.', 'warning')
            return redirect(url_for('get_user', user_id=user_id))

        if User.get_user_by_field('email', email):
            flash('Email já cadastrado, tente fazer login.', 'warning')
            return redirect(url_for('get_user', user_id=user_id))
        
        if password != confirm:
            flash('As senhas não coincidem.', 'warning')
            return redirect(url_for('get_user', user_id=user_id))
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = UserEntity(
            id=user_id,
            role=role,
            email=email,
            username=username,
            created_at=created_at,
            password=hashed_password,
            updated_at=datetime.now(timezone.utc),
        )

        User.update_user(user)
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('get_user', user_id=user_id))


    # DELETE - remove um usuário
    @app.route('/delete_user/<user_id>', methods=['GET'])
    def delete_user(user_id):
        User.delete_user(user_id)
        
        if session.get('user')['id'] == user_id:
            return redirect(url_for('logout'))
        
        flash(f'Usuário deletado com sucesso!', 'success')
        return redirect(url_for('get_users'))
