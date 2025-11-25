from loguru import logger
from dataclasses import dataclass
from typing import List, Optional

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

    @staticmethod
    def get_reviews() -> List[ReviewEntity]:
        try:
            with get_cursor() as cursor:
                cursor.execute("SELECT *, DATE_FORMAT(created_at, '%d/%m/%Y %H:%i:%s') as created_at FROM reviews ORDER BY created_at DES")
                reviews = cursor.fetchall()
                return [ReviewEntity(**u) for u in reviews]
        except Exception as e:
            logger.exception(f"Erro ao buscar avaliações: {e}")
            return []

    @staticmethod
    def get_review_by_field(key: str, value: str) -> Optional[List[ReviewEntity]]:
        try:
            allowed_keys = {"id", "user_id", "book_id", "rating"}
            if key not in allowed_keys:
                raise ValueError(f"Invalid column: {key}")
            with get_cursor() as cursor:
                cursor.execute(f"SELECT * FROM reviews WHERE {key} = %s ORDER BY created_at DESC",(value,))
                if key == 'id':
                    review = cursor.fetchone()
                    return ReviewEntity(**review) if review else None
                reviews = cursor.fetchall()
                return [ReviewEntity(**u) for u in reviews]
        except Exception as e:
            logger.exception(f"Erro ao buscar avaliações: {e}")
            return None

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

    @staticmethod
    def delete_review(id: str) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute("DELETE FROM reviews WHERE id = %s", (id,))
            return True
        except Exception as e:
            logger.exception(f"Erro ao deletar avaliação: {e}")
            return False
