from flask import Flask
from models.book import Book

def configure_routes(app: Flask):

    # GET - retorna todos os livros
    @app.route('/books', methods=['GET'])
    def get_books():
        ...

    # GET - retorna um livro por ID
    @app.route('/books/<book_id>', methods=['GET'])
    def get_book(book_id):
        ...

    # POST - cria um novo livro
    @app.route('/books', methods=['POST'])
    def create_book():
        ...

    # PUT - atualiza um livro
    @app.route('/books/<book_id>', methods=['PUT']) # TODO alterar o método
    def update_book(book_id):
        ...

    # DELETE - remove um livro
    @app.route('/books/<book_id>', methods=['DELETE']) # TODO alterar o método
    def delete_book(book_id):
        ...
