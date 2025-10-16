from flask import Flask
from models.review import Review

def configure_routes(app: Flask):

    # GET - retorna todos as avaliações
    @app.route('/reviews', methods=['GET'])
    def get_reviews():
        ...

    # GET - retorna uma avaliação por ID
    @app.route('/reviews/<review_id>', methods=['GET'])
    def get_review(review_id):
        ...

    # POST - cria uma nova avaliação
    @app.route('/reviews', methods=['POST'])
    def create_review():
        ...

    # PUT - atualiza uma avaliação
    @app.route('/reviews/<review_id>', methods=['PUT']) # TODO alterar o método
    def update_review(review_id):
        ...

    # DELETE - remove uma avaliação
    @app.route('/reviews/<review_id>', methods=['DELETE']) # TODO alterar o método
    def delete_review(review_id):
        ...
