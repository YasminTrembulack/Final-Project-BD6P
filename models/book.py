from loguru import logger
from dataclasses import dataclass
from typing import Dict, List, Optional

from models.db import BaseEntity, get_cursor


@dataclass
class BookEntity(BaseEntity):
    upc: str
    title: str
    img_link: str
    description: str
    category: str


class Book:

    # GET - retorna todos os livros
    @staticmethod
    def get_books() -> List[BookEntity]:
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    "SELECT *, DATE_FORMAT(created_at, '%d/%m/%Y %H:%i:%s') as created_at FROM books ORDER BY title ASC"
                )
                books = cursor.fetchall()
                return [BookEntity(**u) for u in books]
        except Exception as e:
            logger.exception(f"Erro ao buscar livros: {e}")
            return []

    # GET - retorna livros a partir de um campo
    @staticmethod
    def get_book_by_field(key: str, value: str) -> Optional[Dict]:
        try:
            allowed_keys = ["id", "upc", "title", "category"]
            if key not in allowed_keys:
                raise ValueError(f"Invalid column: {key}")
            with get_cursor() as cursor:
                cursor.execute(f"SELECT *, DATE_FORMAT(created_at, '%d/%m/%Y %H:%i:%s') AS created_at FROM books WHERE {key} = %s",(value,))
                book = cursor.fetchall()
                return BookEntity(**book)
        except Exception as e:
            logger.exception(f"Erro ao buscar livros: {e}")
            return None

    # POST - criar livro
    @staticmethod
    def create_book(book: BookEntity) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO books (id, upc, title, img_link, description, category)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (book.id, book.upc, book.title, book.img_link, book.description, book.category),
                )
            return True
        except Exception as e:
            logger.exception(f"Erro ao criar livro: {e}")
            return False

    # PUT - atualizar livro
    @staticmethod
    def update_book(book: BookEntity) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    "UPDATE books SET upc = %s, title = %s, img_link = %s, description = %s, category = %s WHERE id = %s",
                    (book.upc, book.title, book.img_link, book.description, book.category, book.id),
                )
            return True
        except Exception as e:
            logger.exception(f"Erro ao atualizar livro: {e}")
            return False

    # DELETE - deletar livro a partir do ID
    @staticmethod
    def delete_book(id: str) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute("DELETE FROM books WHERE id = %s", (id,))
            return True
        except Exception as e:
            logger.exception(f"Erro ao deletar livro: {e}")
            return False
