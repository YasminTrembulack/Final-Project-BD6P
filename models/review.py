from loguru import logger
from dataclasses import dataclass
from typing import Dict, List, Optional

from models.db import BaseEntity, get_cursor


@dataclass
class ReviewEntity(BaseEntity):
    user_id: str
    book_id: str
    rating: int
    comment: str


class Review:

    # GET - retorna todos as avaliações
    @staticmethod
    def get_reviews() -> List[ReviewEntity]:
        try:
            with get_cursor() as cursor:
                cursor.execute("SELECT *, DATE_FORMAT(created_at, '%d/%m/%Y %H:%i:%s') as created_at FROM reviews ORDER BY created_at ASC")
                reviews = cursor.fetchall()
                return [ReviewEntity(**u) for u in reviews]
        except Exception as e:
            logger.exception(f"Erro ao buscar avaliações: {e}")
            return []

    # GET - retorna avaliações a partir de um campo
    @staticmethod
    def get_review_by_field(key: str, value: str) -> Optional[Dict]:
        try:
            allowed_keys = ["id", "user_id", "book_id", "rating"]
            if key not in allowed_keys:
                raise ValueError(f"Invalid column: {key}")
            with get_cursor() as cursor:
                cursor.execute(f"SELECT *, DATE_FORMAT(created_at, '%d/%m/%Y %H:%i:%s') AS created_at FROM reviews WHERE {key} = %s",(value,))
                review = cursor.fetchall()
                return ReviewEntity(**review)
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
                    "UPDATE reviews SET upc = %s, title = %s, img_link = %s, description = %s, category = %s WHERE id = %s",
                    (review.upc, review.title, review.img_link, review.description, review.category, review.id),
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
