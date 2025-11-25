import os
from io import BytesIO
from uuid import uuid4

import requests
from faker import Faker
from werkzeug.utils import secure_filename
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from models.book import Book, BookEntity
from models.review import Review
from models.user import User


# ==============================
# ⚙️ CONFIGURAÇÕES INICIAIS
# ==============================
fake = Faker("pt_BR")  # gera texto fictício em português
UPLOAD_FOLDER = r'C:\Users\yastr\Desktop\Projects\Final-Project-BD6P\views\static\cover_uploads'


def configure_routes(app: Flask):
    """
    Configura todas as rotas relacionadas a livros.
    """


    # ==========================================================
    # 📚 GET - Lista todos os livros (com paginação)
    # ==========================================================
    @app.route('/get_books', methods=['GET'])
    def get_books():
        per_page = 20
        page = int(request.args.get('page', 1)) if session.get('user') else 1

        # Busca os livros paginados
        books_response = Book.get_books(page, per_page)
        pagination = books_response['pagination'].to_dict()
        total_pages = pagination['total_pages']

        # Define intervalo de páginas visíveis
        start_page = max(1, page - 2)
        end_page = min(total_pages, page + 2)

        books = books_response['data']
        categories = Book.list_distinct_categories()

        # Se estiver atualizando um livro, busca ele
        update_book = Book.get_book_by_field('id', request.args.get("book_id"))

        return render_template(
            'books.html',
            logged_user=session.get('user'),
            books=books,
            categories=categories,
            book_to_update=update_book,
            pagination_info=pagination,
            start_page=start_page,
            end_page=end_page,
            empty_cards=(4 - (len(books) % 4)) % 4  # completa grid com espaços vazios
        )


    # ==========================================================
    # 📖 GET - Retorna detalhes de um livro específico
    # ==========================================================
    @app.route('/get_book/<book_id>', methods=['GET'])
    def get_book(book_id):
        book = Book.get_book_by_field('id', book_id)
        update_review = Review.get_review_by_field('id', request.args.get("review_id"))

        # Busca as avaliações do livro
        reviews = Review.get_review_by_field('book_id', book_id)
        if reviews:
            for review in reviews:
                review.user = User.get_user_by_field('id', review.user_id)

        return render_template(
            'book-details.html',
            logged_user=session.get('user'),
            book=book,
            reviews=reviews,
            review_to_update=update_review
        )


    # ==========================================================
    # ➕ POST/GET - Cria um novo livro
    # ==========================================================
    @app.route('/create_book', methods=['GET', 'POST'])
    def create_book():
        """
        Cria uma novo livro (titulo, autor, código UPC, categoria, descrição e imagem da capa).
        - GET → Renderiza o formulário de criação.
        - POST → Recebe os dados e insere o livro no banco.
        """
        # Formulário de criação
        if request.method == 'GET':
            categories = Book.list_distinct_categories()
            return render_template('upsert-book.html',
                                   logged_user=session.get('user'),
                                   categories=categories)

        # --- Dados do formulário ---
        category = request.form.get('category')
        upc = request.form.get('upc')
        cover = request.files.get('cover')
        book_id = str(uuid4())
        img_link = None

        # Verifica se o código UPC já existe
        if Book.get_book_by_field('upc', upc):
            flash('Livro com esse código UPC já cadastrado!', 'warning')
            return redirect(url_for('create_book'))

        # Salva a imagem de capa (se houver)
        if cover:
            filename = secure_filename(cover.filename)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{book_id}{ext}"
            img_link = f"cover_uploads/{new_filename}"
            file_path = os.path.join(UPLOAD_FOLDER, new_filename)
            cover.save(file_path)

        # Cria o objeto e insere no banco
        new_book = BookEntity(
            id=book_id,
            title=request.form.get('title'),
            author=request.form.get('author'),
            upc=upc,
            category=category or None,
            description=request.form.get('description'),
            img_link=img_link
        )
        Book.create_book(new_book)

        flash('Livro criado com sucesso!', 'success')
        return redirect(url_for('get_books'))


    # ==========================================================
    # ✏️ PUT/GET - Atualiza um livro existente
    # ==========================================================
    @app.route('/update_book/<book_id>', methods=['GET', 'POST'])
    def update_book(book_id):
        """
        Atualiza um livro existente.
        - GET → Exibe o formulário preenchido com os dados atuais.
        - POST → Salva as alterações no banco.
        """
        # Exibe o formulário com dados atuais
        if request.method == 'GET':
            book_to_update = Book.get_book_by_field('id', book_id)
            categories = Book.list_distinct_categories()
            return render_template(
                'upsert-book.html',
                logged_user=session.get('user'),
                book_to_update=book_to_update,
                categories=categories
            )

        # --- Atualização ---
        category = request.form.get('category')
        upc = request.form.get('upc')
        cover = request.files.get('cover')
        img_link = None

        # Verifica duplicidade de UPC
        existing_book = Book.get_book_by_field('upc', upc)
        if existing_book and existing_book.id != book_id:
            flash('Livro com esse código UPC já cadastrado!', 'warning')
            return redirect(url_for('get_books'))

        # Atualiza ou mantém capa
        if cover:
            filename = secure_filename(cover.filename)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{book_id}{ext}"
            img_link = f"cover_uploads/{new_filename}"
            file_path = os.path.join(UPLOAD_FOLDER, new_filename)
            cover.save(file_path)
        else:
            img_link = Book.get_book_by_field('id', book_id).img_link

        # Atualiza o registro
        updated_book = BookEntity(
            id=book_id,
            title=request.form.get('title'),
            author=request.form.get('author'),
            upc=upc,
            category=category or None,
            description=request.form.get('description'),
            img_link=img_link
        )
        Book.update_book(updated_book)

        flash('Livro atualizado com sucesso!', 'success')
        return redirect(url_for('get_books'))


    # ==========================================================
    # ❌ DELETE - Remove um livro
    # ==========================================================
    @app.route('/delete_book/<book_id>', methods=['GET'])
    def delete_book(book_id):
        book = Book.get_book_by_field('id', book_id)

        # Remove o arquivo da capa local
        if book and book.img_link:
            filename = book.img_link.replace('cover_uploads/', '')
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Remove do banco
        Book.delete_book(book_id)
        flash('Livro deletado com sucesso!', 'success')
        return redirect(url_for('get_books'))


    # ==========================================================
    # 📄 DOWNLOAD - Gera PDF de amostra do livro
    # ==========================================================
    @app.route("/download_sample/<book_id>")
    def download_sample(book_id):
        # Busca o livro no banco a partir do ID fornecido pela rota
        book = Book.get_book_by_field("id", book_id)

        # Cria um buffer em memória para gerar o PDF sem salvar arquivo em disco
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4  # Dimensões da página

        # ---------------------------------------------------------
        # Página 1 — capa da amostra
        # ---------------------------------------------------------

        # Título do livro em destaque
        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawCentredString(width / 2, height - 80, book.title)

        # Autor do livro
        pdf.setFont("Helvetica", 14)
        pdf.drawCentredString(width / 2, height - 110, f"por {book.author}")

        # Pequeno trecho da descrição do livro
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, height - 160, (book.description or "Nenhuma descrição disponível.")[:100])
        # limita a 100 caracteres
        
        # Avança para a próxima página
        pdf.showPage()

        # ---------------------------------------------------------
        # Página 2 — início fictício do capítulo
        # ---------------------------------------------------------

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, height - 60, "Capítulo 1")

        # Texto da amostra gerado automaticamente
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, height - 100, "Este é apenas um trecho de amostra gerado automaticamente.")

        # Finaliza e grava o conteúdo do PDF
        pdf.save()
        buffer.seek(0)

        # Criação da resposta HTTP com cabeçalhos apropriados para download
        response = make_response(buffer.getvalue())
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = (f"attachment; filename=amostra_{book.upc}.pdf")

        return response
