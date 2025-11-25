from datetime import datetime, timezone
import bcrypt

from loguru import logger

from flask import Flask, flash, redirect, render_template, request, session, url_for
from models.user import User, UserEntity

def configure_routes(app: Flask):

    @app.route('/get_users', methods=['GET'])
    def get_users():
        per_page = 20
        page = int(request.args.get('page', 1)) if session.get('user') else 1
        
        users_response = User.get_users(page, per_page)
        pagination = users_response['pagination'].to_dict()
        total_pages = pagination['total_pages']

        start_page = max(1, page - 2)
        end_page = min(total_pages, page + 2)
        
        users = users_response['data']

        return render_template(
            'users.html',
            empty_cards=(3 - (len(users) % 3)) % 3,
            logged_user=session.get('user'),
            pagination_info=pagination,
            start_page=start_page,
            end_page=end_page,
            users=users,
        )


    @app.route('/get_user/<user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.get_user_by_field('id', user_id)
        logged_user = session.get('user', {})
        
        if not logged_user or user.id != logged_user.get('id'):
            user = None
            if logged_user:
                flash('Acesso negado: faça login com a conta correspondente visualizar o perfil.', 'warning')
                user = User.get_user_by_field('id', logged_user.get('id'))

        return render_template(
            'profile.html',
            user=user,
        )


    @app.route('/create_user', methods=['GET', 'POST'])
    def create_user():
        if request.method == 'GET':
            return render_template('upsert-user.html')

        try:
            form = request.form
            username = form.get('username', '').strip()
            email = form.get('email', '').strip()
            password = form.get('password')
            confirm = form.get('confirm-password')
            role = form.get('role') or 'user'

            if not username or not email or not password or not confirm:
                flash('Todos os campos são obrigatórios.', 'warning')
                return redirect(url_for('create_user'))

            if User.get_user_by_field('username', username):
                flash('Nome de usuário já utilizado, escolha outro.', 'warning')
                return redirect(url_for('create_user'))

            if User.get_user_by_field('email', email):
                flash('Email já cadastrado, tente fazer login.', 'warning')
                return redirect(url_for('create_user'))

            if password != confirm:
                flash('As senhas não coincidem.', 'warning')
                return redirect(url_for('create_user'))

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
            return redirect(url_for('create_user'))


    @app.route('/update_user_role/<user_id>', methods=['GET', 'POST'])
    def update_user_role(user_id):
        role = request.form.get('role')
        
        user = User.get_user_by_field('id', user_id)
        if not user:
            flash('Usuário não encontrado.', 'error')
            return redirect(url_for('get_users'))

        updated_user = UserEntity(
            id=user_id,
            role=role,
            email=user.email,
            username=user.username,
            created_at=user.created_at,
            password=user.password,
            updated_at=datetime.now(timezone.utc),
        )

        User.update_user(updated_user)
        flash(f'Role de {user.username} atualizado com sucesso!', 'success')
        return redirect(url_for('get_users'))

    
    @app.route('/update_user/<user_id>', methods=['GET', 'POST'])
    def update_user(user_id):
        user = User.get_user_by_field('id', user_id)
        logged_user = session.get('user', {})

        if request.method == 'GET':
            if not logged_user:
                return redirect(url_for('get_books'))
            
            if user.id != logged_user.get('id'):
                flash('Acesso negado: faça login com a conta correspondente para atualizar este usuário.', 'warning')
                return redirect(url_for('get_user', user_id=logged_user.get('id')))
    
            return render_template(
                'upsert-user.html', 
                user=user, 
                logged_user=logged_user
            )

        if not user:
            flash('Usuário não encontrado.', 'error')
            return redirect(url_for('get_users'))

        form = request.form
        username = form.get('username', '').strip()
        role = form.get('role', '')
        email = form.get('email', '').strip()
        password = form.get('password')
        confirm = form.get('confirm-password')

        existing_user = User.get_user_by_field('username', username)
        if existing_user and existing_user.id != user_id:
            flash('Nome de usuário já utilizado, escolha outro.', 'warning')
            return redirect(url_for('update_user', user_id=user_id))

        existing_email = User.get_user_by_field('email', email)
        if existing_email and existing_email.id != user_id:
            flash('Email já cadastrado, tente outro.', 'warning')
            return redirect(url_for('update_user', user_id=user_id))

        if not password:
            hashed_password = user.password
        elif password != confirm:
            flash('As senhas não coincidem.', 'warning')
            return redirect(url_for('update_user', user_id=user_id))
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        updated_user = UserEntity(
            id=user_id,
            role=role or user.role,
            email=email or user.email,
            username=username or user.username,
            created_at=user.created_at,
            password=hashed_password,
            updated_at=datetime.now(timezone.utc),
        )

        session_user = session.get('user', {})
        session_user.update({
            "username": updated_user.username,
            "email": updated_user.email,
            "role": updated_user.role,
        })
        session['user'] = session_user

        User.update_user(updated_user)
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('get_user', user_id=user_id))


    @app.route('/delete_user/<user_id>', methods=['GET'])
    def delete_user(user_id):
        User.delete_user(user_id)

        if session.get('user')['id'] == user_id:
            return redirect(url_for('logout'))

        flash(f'Usuário deletado com sucesso!', 'success')
        return redirect(url_for('get_users'))
