from flask import Flask, flash, redirect, render_template, request, session, url_for
from models.review import Review, ReviewEntity

def configure_routes(app: Flask):
    """
    Configura todas as rotas relacionadas às avaliações de livros.
    Inclui criação, atualização e exclusão de reviews.
    """


    # ==========================================================
    # 📖 GET - Retorna comentários de um livro específico
    # ==========================================================
    #? O GET de reviews esta presenta no get_book de Livros, onde é possivel visualiar detalhes do livro e seus comentários.


    # ==========================================================
    # ➕ POST/GET - Criar nova avaliação (Review)
    # ==========================================================
    @app.route('/create_review/<book_id>', methods=['GET', 'POST'])
    def create_review(book_id):
        """
        Cria uma nova avaliação (comentário + nota) para um livro específico.
        - GET → Renderiza o formulário de criação.
        - POST → Recebe os dados e insere a avaliação no banco.
        """

        if request.method == 'GET':
            # Exibe o formulário de criação de avaliação
            return render_template(
                'upsert-review.html',
                book_id=book_id,
                logged_user=session.get('user'),
            )

        # Obtém dados do formulário
        comment = request.form.get('comment')
        rating = request.form.get('rating')
        user = session.get('user')

        # Cria a entidade de avaliação
        new_review = ReviewEntity(
            book_id=book_id,
            user_id=user['id'],
            rating=rating,
            comment=comment,
        )

        # Persiste no banco
        Review.create_review(new_review)
        
        flash("Avaliação registrada com sucesso!", 'success')

        # Retorna para a página do livro
        return redirect(url_for('get_book', book_id=book_id))


    # ==========================================================
    # ✏️ PUT/GET - Atualizar uma avaliação existente
    # ==========================================================
    @app.route('/update_review/<review_id>/', methods=['GET', 'POST'])
    def update_review(review_id):
        """
        Atualiza uma avaliação existente.
        - GET → Exibe o formulário preenchido com os dados atuais.
        - POST → Salva as alterações no banco.
        """

        # Busca a avaliação existente
        review_to_update = Review.get_review_by_field('id', review_id)

        if request.method == 'GET':
            # Exibe o formulário de edição com dados atuais
            return render_template(
                'upsert-review.html',
                logged_user=session.get('user'),
                review_to_update=review_to_update,
            )

        # Obtém o ID do livro para redirecionamento posterior
        book_id = review_to_update.book_id

        # Coleta novos dados do formulário
        comment = request.form.get('comment')
        rating = request.form.get('rating')
        user = session.get('user')

        # Cria nova entidade atualizada
        updated_review = ReviewEntity(
            id=review_id,
            book_id=book_id,
            user_id=user['id'],
            rating=rating,
            comment=comment,
        )

        # Atualiza no banco
        Review.update_review(updated_review)

        flash(f'Avaliação atualizada com sucesso!', 'success')
        
        # Redireciona de volta para o livro
        return redirect(url_for('get_book', book_id=book_id))


    # ==========================================================
    # ❌ DELETE - Remover uma avaliação
    # ==========================================================
    @app.route('/delete_review/<review_id>', methods=['GET'])
    def delete_review(review_id):
        """
        Remove uma avaliação com base no seu ID.
        Após a exclusão, redireciona de volta para a página do livro.
        """

        # Exclui a avaliação
        Review.delete_review(review_id)

        # Obtém o ID do livro (enviado como query param)
        book_id = request.args.get("book_id")

        flash(f'Avaliação deletada com sucesso!', 'success')

        # Redireciona de volta para os detalhes do livro
        return redirect(url_for('get_book', book_id=book_id))
