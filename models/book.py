from loguru import logger
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from models.db import BaseEntity, get_cursor
from models.pagination import PaginationInfo


@dataclass
class BookEntity(BaseEntity):
    upc: str
    title: str
    author: str
    img_link: Optional[str]
    description: Optional[str]
    category: Optional[str]


class Book:
    @staticmethod
    def get_books(page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        try:
            offset = (page - 1) * per_page

            with get_cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS total FROM books")
                total_books = cursor.fetchone()["total"]

                cursor.execute("SELECT * FROM books ORDER BY created_at ASC LIMIT %s OFFSET %s", (per_page, offset))
                books = cursor.fetchall()

            pagination = PaginationInfo(
                page=page,
                per_page=per_page,
                total_items=total_books
            )

            return {
                "data": [BookEntity(**book) for book in books],
                "pagination": pagination,
            }

        except Exception as e:
            logger.exception(f"Erro ao buscar livros paginados: {e}")
            return {"data": [], "pagination": PaginationInfo(page, per_page, 0)}

    @staticmethod
    def list_distinct_categories() -> Optional[List[str]]:
        try:
            with get_cursor() as cursor:
                cursor.execute(f"SELECT DISTINCT category FROM books;")
                categories = cursor.fetchall()
                return [category['category'] for category in categories]
        except Exception as e:
            logger.exception(f"Erro ao buscar categorias dos livros: {e}")
            return None
    
    @staticmethod
    def get_book_by_field(key: str, value: str) -> Optional[List[BookEntity]] | Optional[BookEntity]:
        try:
            allowed_keys = {"id", "upc", "title", "category", "author"}
            if key not in allowed_keys:
                raise ValueError(f"Invalid column: {key}")
            with get_cursor() as cursor:
                cursor.execute(f"SELECT * FROM books WHERE {key} = %s",(value,))
                if key in {"id", "upc"}:
                    book = cursor.fetchone()
                    return BookEntity(**book) if book else None
                    
                books = cursor.fetchall()
                return [BookEntity(**book) for book in books]
        except Exception as e:
            logger.exception(f"Erro ao buscar livros: {e}")
            return None

    @staticmethod
    def create_book(book: BookEntity) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO books (id, upc, title, author, img_link, description, category)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (book.id, book.upc, book.title, book.author, book.img_link, book.description, book.category),
                )
            return True
        except Exception as e:
            logger.exception(f"Erro ao criar livro: {e}")
            return False

    @staticmethod
    def update_book(book: BookEntity) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    "UPDATE books SET upc = %s, title = %s, author = %s, img_link = %s, description = %s, category = %s WHERE id = %s",
                    (book.upc, book.title, book.author, book.img_link, book.description, book.category, book.id),
                )
            return True
        except Exception as e:
            logger.exception(f"Erro ao atualizar livro: {e}")
            return False

    @staticmethod
    def delete_book(id: str) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute("DELETE FROM books WHERE id = %s", (id,))
            return True
        except Exception as e:
            logger.exception(f"Erro ao deletar livro: {e}")
            return False
