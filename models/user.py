from loguru import logger
from dataclasses import dataclass
from typing import Dict, List, Optional

from models.db import BaseEntity, get_cursor


@dataclass
class UserEntity(BaseEntity):
    username: str
    password: str
    email: str
    role: str


class User:

    # GET - retorna todos os usuários
    @staticmethod
    def get_users() -> List[UserEntity]:
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    "SELECT *, DATE_FORMAT(created_at, '%d/%m/%Y %H:%i:%s') as created_at FROM users ORDER BY full_name ASC"
                )
                users = cursor.fetchall()
                return [UserEntity(**u) for u in users]
        except Exception as e:
            logger.exception(f"Erro ao buscar usuários: {e}")
            return []

    # GET - retorna usuários a partir de um campo
    @staticmethod
    def get_user_by_field(key: str, value: str) -> Optional[Dict]:
        try:
            allowed_keys = ["id", "username", "email", "role"]
            if key not in allowed_keys:
                raise ValueError(f"Invalid column: {key}")
            with get_cursor() as cursor:
                cursor.execute(f"SELECT *, DATE_FORMAT(created_at, '%d/%m/%Y %H:%i:%s') AS created_at FROM users WHERE {key} = %s",(value,))
                user = cursor.fetchall()
                return UserEntity(**user)
        except Exception as e:
            logger.exception(f"Erro ao buscar usuários: {e}")
            return None

    # POST - criar usuário
    @staticmethod
    def create_user(user: UserEntity) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO users (id, username, password, email, role)
                        VALUES (%s, %s, %s, %s)
                    """, (user.id, user.username, user.password, user.email, user.role),
                )
            return True
        except Exception as e:
            logger.exception(f"Erro ao criar usuário: {e}")
            return False

    # PUT - atualizar usuário
    @staticmethod
    def update_user(user: UserEntity) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET full_name = %s, email = %s, password = %s, role = %s WHERE id = %s",
                    (user.username, user.email, user.password, user.role, user.id),
                )
            return True
        except Exception as e:
            logger.exception(f"Erro ao atualizar usuário: {e}")
            return False

    # DELETE - deletar usuário a partir do ID
    @staticmethod
    def delete_user(id: str) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (id,))
            return True
        except Exception as e:
            logger.exception(f"Erro ao deletar usuário: {e}")
            return False
