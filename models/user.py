from typing import List

from loguru import logger

from config import DB_NAME
from models.db import get_cursor


class User():
    
    @staticmethod
    def get_users() -> List:
        try:
            with get_cursor() as cursor:
                cursor.execute(f"SELECT *, DATE_FORMAT(created_at, '%d/%m/%Y %H:%i:%s') as created_at FROM {DB_NAME}.users ORDER BY created_at ASC")
                return cursor.fetchall()
        except Exception as e:
            logger.exception(f"Erro ao buscar tarefas: {e}")
            return []