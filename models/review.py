from loguru import logger
from dataclasses import dataclass
from typing import Dict, List, Optional

from models.book import BookEntity
from models.db import BaseEntity, get_cursor
from models.user import UserEntity


@dataclass
class ReviewEntity(BaseEntity):
    user_id: str
    book_id: str
    rating: int
    comment: str
    user: Optional[UserEntity] = None
    book: Optional[BookEntity] = None


class Review:

    # GET - retorna todos as avaliações
    @staticmethod
    def get_reviews() -> List[ReviewEntity]:
        try:
            with get_cursor() as cursor:
                cursor.execute("SELECT *, DATE_FORMAT(created_at, '%d/%m/%Y %H:%i:%s') as created_at FROM reviews ORDER BY created_at DESC")
                reviews = cursor.fetchall()
                return [ReviewEntity(**u) for u in reviews]
        except Exception as e:
            logger.exception(f"Erro ao buscar avaliações: {e}")
            return []

    # GET - retorna avaliações a partir de um campo
    @staticmethod
    def get_review_by_field(key: str, value: str) -> Optional[List[ReviewEntity]]:
        try:
            queries = {
                "id": "SELECT * FROM reviews WHERE id = %s ORDER BY created_at DESC",
                "user_id": "SELECT * FROM reviews WHERE user_id = %s ORDER BY created_at DESC",
                "book_id": "SELECT * FROM reviews WHERE book_id = %s ORDER BY created_at DESC",
                "rating": "SELECT * FROM reviews WHERE rating = %s ORDER BY created_at DESC",
            }

            if key not in queries:
                raise ValueError(f"Invalid column: {key}")

            with get_cursor() as cursor:
                cursor.execute(queries[key], (value,))

                if key == "id":
                    review = cursor.fetchone()
                    return ReviewEntity(**review) if review else None

                reviews = cursor.fetchall()
                return [ReviewEntity(**u) for u in reviews]

        except Exception as e:
            logger.exception(f"Erro ao buscar avaliações: {e}")
            return None

    # POST - criar avaliação
    @staticmethod
    def create_review(review: ReviewEntity) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO reviews (id, user_id, book_id, rating, comment)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (review.id, review.user_id, review.book_id, review.rating, review.comment,),
                )
            return True
        except Exception as e:
            logger.exception(f"Erro ao criar avaliação: {e}")
            return False

    # PUT - atualizar avaliação
    @staticmethod
    def update_review(review: ReviewEntity) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    "UPDATE reviews SET user_id = %s, book_id = %s, rating = %s, comment = %s WHERE id = %s",
                    (review.user_id, review.book_id, review.rating, review.comment, review.id),
                )
            return True
        except Exception as e:
            logger.exception(f"Erro ao atualizar avaliação: {e}")
            return False

    # DELETE - deletar avaliação a partir do ID
    @staticmethod
    def delete_review(id: str) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute("DELETE FROM reviews WHERE id = %s", (id,))
            return True
        except Exception as e:
            logger.exception(f"Erro ao deletar avaliação: {e}")
            return False
