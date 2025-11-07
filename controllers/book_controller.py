import os
from uuid import uuid4
from flask import Flask, flash, redirect, render_template, request, session, url_for
from models.book import Book, BookEntity
from models.review import Review
from models.user import User
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:\\Users\\yastr\\Desktop\\Projects\\Final-Project-BD6P\\views\\static\\cover_uploads'


def configure_routes(app: Flask):

    # GET - retorna todos os livros
    @app.route('/get_books', methods=['GET'])
    def get_books():
        per_page = 20
        page = int(request.args.get('page', 1)) if session.get('user') else 1
        books_response = Book.get_books(page ,per_page)
        
        pagination = books_response['pagination'].to_dict()
        total_pages = pagination['total_pages']

        start_page = max(1, page - 2)
        end_page = min(total_pages, page + 2)
        
        books = books_response['data']
        categories = Book.list_distinct_categories()
        
        update_book = Book.get_book_by_field('id', request.args.get("book_id"))

        return render_template(
            'books.html',
            empty_cards= (4 - (len(books) % 4)) % 4,
            logged_user=session.get('user'),
            pagination_info=pagination,
            book_to_update=update_book,
            start_page=start_page,
            categories=categories,
            end_page=end_page,
            books=books,
        )

    # GET - retorna um livro por ID
    @app.route('/get_book/<book_id>', methods=['GET'])
    def get_book(book_id):
        book = Book.get_book_by_field('id', book_id)
        
        update_review = Review.get_review_by_field('id', request.args.get("review_id"))

        # GET - retorna todos as avaliações por livro
        reviews = Review.get_review_by_field('book_id', book_id)
        
        if reviews:
            for review in reviews:
                review.user = User.get_user_by_field('id', review.user_id)
        
        return render_template(
            'book-details.html',
            logged_user=session.get('user'),  
            review_to_update=update_review,  
            reviews=reviews,
            book=book
        )

    # POST - cria um novo livro
    @app.route('/create_book', methods=['POST'])
    def create_book():
        category = request.form.get('category')
        upc = request.form.get('upc')
        cover = request.files['cover']
        img_link = None
        book_id = str(uuid4())
        
        if Book.get_book_by_field('upc', upc):
            flash('Livro com esse código UPC já cadastrado!', 'warning')
            return redirect(url_for('get_books'))

        if cover:
            filename = secure_filename(cover.filename)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{book_id}{ext}"
            img_link = f"cover_uploads/{new_filename}"
            
            file_path = os.path.join(UPLOAD_FOLDER, new_filename)
            cover.save(file_path)
            
        new_book = BookEntity(
            id=book_id,
            title=request.form.get('title'),
            author=request.form.get('author'),
            upc=request.form.get('upc'),
            category=category or None,
            description=request.form.get('description'),
            img_link=img_link 
        )
        Book.create_book(new_book)
        flash(f'Livro criado com sucesso!', 'success')
        return redirect(url_for('get_books'))

    # PUT - atualiza um livro
    @app.route('/update_book/<book_id>', methods=['POST'])
    def update_book(book_id):
        category = request.form.get('category')
        upc = request.form.get('upc')
        cover = request.files['cover']
        img_link = None
        
        if Book.get_book_by_field('upc', upc).id != book_id:
            flash('Livro com esse código UPC já cadastrado!', 'warning')
            return redirect(url_for('get_books'))

        if cover:
            filename = secure_filename(cover.filename)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{book_id}{ext}"
            img_link = f"cover_uploads/{new_filename}"
            
            file_path = os.path.join(UPLOAD_FOLDER, new_filename)
            cover.save(file_path)
        else: 
            book = Book.get_book_by_field('id', book_id)
            img_link = book.img_link
            
        new_book = BookEntity(
            id=book_id,
            title=request.form.get('title'),
            author=request.form.get('author'),
            upc=request.form.get('upc'),
            category=category or None,
            description=request.form.get('description'),
            img_link=img_link 
        )
        Book.update_book(new_book)
        flash(f'Livro atualizado com sucesso!', 'success')
        return redirect(url_for('get_books'))

    # DELETE - remove um livro
    @app.route('/delete_book/<book_id>', methods=['GET'])
    def delete_book(book_id):
        book = Book.get_book_by_field('id', book_id)
        filename = book.img_link.replace('cover_uploads/', '')
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        if os.path.exists(file_path):
            os.remove(file_path)

        Book.delete_book(book_id)
        
        flash(f'Livro deletado com sucesso!', 'success')
        return redirect(url_for('get_books'))
