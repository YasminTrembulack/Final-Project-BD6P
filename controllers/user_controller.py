from flask import Flask
from models.user import User

def configure_routes(app: Flask):

    # GET - retorna todos os usuários
    @app.route('/users', methods=['GET'])
    def get_users():
        ...

    # GET - retorna um usuário por ID
    @app.route('/users/<user_id>', methods=['GET'])
    def get_user(user_id):
        ...

    # POST - cria um novo usuário
    @app.route('/users', methods=['POST'])
    def create_user():
        ...

    # PUT - atualiza um usuário
    @app.route('/users/<user_id>', methods=['PUT']) # TODO alterar o método
    def update_user(user_id):
        ...

    # DELETE - remove um usuário
    @app.route('/users/<user_id>', methods=['DELETE']) # TODO alterar o método
    def delete_user(user_id):
        ...
