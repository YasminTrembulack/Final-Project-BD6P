from flask import Flask, redirect, request, session, url_for
from models.review import Review, ReviewEntity

def configure_routes(app: Flask):
    # @app.route('/reviews', methods=['GET'])
    # def get_reviews():
    #     ...
    
    # @app.route('/reviews/<review_id>', methods=['GET'])
    # def get_review(review_id):
    #     ...

    # POST - cria uma nova avaliação
    @app.route('/create_review', methods=['POST'])
    def create_review():
        book_id = request.form.get('book_id')
        comment = request.form.get('comment')
        rating = request.form.get('rating')
        user = session.get('user')

        new_review = ReviewEntity(
            book_id=book_id,
            user_id=user['id'],
            rating=rating,
            comment=comment,
        )

        Review.create_review(new_review)

        return redirect(url_for('get_book', book_id=book_id))

    # PUT - atualiza uma avaliação
    @app.route('/update_review/<review_id>/', methods=['GET', 'POST'])
    def update_review(review_id):
        book_id = request.form.get('book_id')
        comment = request.form.get('comment')
        rating = request.form.get('rating')
        user = session.get('user')

        new_review = ReviewEntity(
            id=review_id,
            book_id=book_id,
            user_id=user['id'],
            rating=rating,
            comment=comment,
        )

        Review.update_review(new_review)

        return redirect(url_for('get_book', book_id=book_id))


    # DELETE - remove uma avaliação
    @app.route('/delete_review/<review_id>', methods=['GET']) # TODO alterar o método
    def delete_review(review_id):
        Review.delete_review(review_id)
        book_id = request.args.get("book_id")
        return redirect(url_for('get_book', book_id=book_id))
