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
    @app.route('/download_sample/<book_id>', methods=['GET'])
    def download_sample(book_id):
        book = Book.get_book_by_field('id', book_id)
        
        # Cria o PDF em memória
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # =======================
        # 🎨 CAPA DO LIVRO
        # =======================
        pdf.setTitle(f"Amostra - {book.title}")

        # Fundo da capa
        pdf.setFillColorRGB(0.95, 0.95, 0.95)
        pdf.rect(0, 0, width, height, fill=True, stroke=False)

        # Título centralizado
        pdf.setFont("Helvetica-Bold", 22)
        pdf.setFillColor(colors.HexColor("#222222"))
        pdf.drawCentredString(width / 2, height - 100, book.title)

        # Autor
        pdf.setFont("Helvetica", 14)
        pdf.setFillColor(colors.HexColor("#444444"))
        pdf.drawCentredString(width / 2, height - 130, f"por {book.author}")

        # Imagem da capa (se existir)
        if book.img_link:
            try:
                if book.img_link.startswith("cover_uploads/"):
                    local_path = os.path.join("views", "static", book.img_link.replace("/", os.sep))
                    print(local_path)
                    if os.path.exists(local_path):
                        img = ImageReader(local_path)
                    else:
                        print(f"Imagem local não encontrada: {local_path}")
                else:
                    # tenta carregar imagem online
                    response = requests.get(book.img_link, stream=True, timeout=5)
                    if response.status_code == 200:
                        img = ImageReader(BytesIO(response.content))

                if img:
                    img_width, img_height = 200, 280
                    pdf.drawImage(
                        img,
                        (width - img_width) / 2,
                        height - 450,
                        width=img_width,
                        height=img_height,
                        preserveAspectRatio=True,
                        mask='auto'
                    )
            except Exception as e:
                print(f"Erro ao carregar imagem: {e}")

        # Linha decorativa
        pdf.setStrokeColor(colors.HexColor("#888888"))
        pdf.line(80, height - 470, width - 80, height - 470)

        # Texto introdutório
        pdf.setFont("Helvetica-Oblique", 12)
        pdf.setFillColor(colors.HexColor("#555555"))
        pdf.drawCentredString(width / 2, height - 500, "Amostra gratuita do livro")

        # =======================
        # 📖 CONTEÚDO (descrição)
        # =======================
        pdf.showPage()  # nova página
        pdf.setFont("Helvetica-Bold", 16)
        pdf.setFillColor(colors.HexColor("#222222"))
        pdf.drawString(70, height - 80, "Resumo do Livro")

        def dividir_texto(texto, largura_max):
            """Quebra texto em linhas menores para caber no PDF"""
            palavras = texto.split()
            linha, linhas = "", []
            for palavra in palavras:
                if pdf.stringWidth(linha + " " + palavra, "Helvetica", 12) < largura_max:
                    linha += " " + palavra
                else:
                    linhas.append(linha.strip())
                    linha = palavra
            linhas.append(linha.strip())
            return linhas

        pdf.setFont("Helvetica", 12)
        pdf.setFillColor(colors.HexColor("#333333"))
        y = height - 120
        max_width = width - 140

        if book.description:
            for line in dividir_texto(book.description, max_width):
                pdf.drawString(70, y, line)
                y -= 18
                if y < 80:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 12)
                    y = height - 80
        else:
            pdf.drawString(70, y, "Nenhuma descrição disponível para este livro.")
            
        # =======================
        # 📘 CAPÍTULO 1 (texto simulado)
        # =======================
        pdf.showPage()
        pdf.setFont("Helvetica-Bold", 16)
        pdf.setFillColor(colors.HexColor("#222222"))
        pdf.drawString(70, height - 80, "Capítulo 1")

        # Gera texto fictício para simular o início do livro
        chapter_text = "\n\n".join(fake.paragraph() for _ in range(40))

        pdf.setFont("Helvetica", 12)
        pdf.setFillColor(colors.HexColor("#333333"))
        y = height - 120
        max_width = width - 140

        for line in dividir_texto(chapter_text, max_width):
            pdf.drawString(70, y, line)
            y -= 18
            if y < 80:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y = height - 80

        # =======================
        # 📄 Rodapé
        # =======================
        pdf.setFont("Helvetica-Oblique", 10)
        pdf.setFillColor(colors.HexColor("#666666"))
        pdf.drawCentredString(width / 2, 40, "Gerado automaticamente por LitScore © 2025")

        pdf.save()
        buffer.seek(0)

        # Retorna o PDF como arquivo para download
        response = make_response(buffer.getvalue())
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = f"attachment; filename=amostra_{book.upc}.pdf"
        return response
