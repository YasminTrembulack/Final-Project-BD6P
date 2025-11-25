from loguru import logger
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from models.db import BaseEntity, get_cursor
from models.pagination import PaginationInfo


@dataclass
class UserEntity(BaseEntity):
    username: str
    password: str
    email: str
    role: str


class User:

    @staticmethod
    def get_users(page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        try:
            offset = (page - 1) * per_page
            with get_cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS total FROM users")
                total_users = cursor.fetchone()["total"]
                cursor.execute("SELECT * FROM users ORDER BY created_at ASC LIMIT %s OFFSET %s", (per_page, offset))
                users = cursor.fetchall()
                
            pagination = PaginationInfo(
                page=page,
                per_page=per_page,
                total_items=total_users
            )
            
            return {
                "data": [UserEntity(**user) for user in users],
                "pagination": pagination,
            }
        except Exception as e:
            logger.exception(f"Erro ao buscar usuários: {e}")
            return []

    @staticmethod
    def get_user_by_field(key: str, value: str) -> Optional[List[UserEntity]] | Optional[UserEntity]:
        try:
            allowed_keys = {"id", "username", "email", "role"}
            if key not in allowed_keys:
                raise ValueError(f"Invalid column: {key}")
            with get_cursor() as cursor:
                cursor.execute(f"SELECT * FROM final_project_db.users WHERE {key} = %s", (value,))
                if key == 'role':
                    return [UserEntity(**u) for u in cursor.fetchall()]
                user = cursor.fetchone()
                return UserEntity(**user) if user else None
        except Exception as e:
            logger.exception(f"Erro ao buscar usuários: {e}")
            return None

    @staticmethod
    def create_user(user: UserEntity) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO final_project_db.users (id, username, password, email, role)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (user.id, user.username, user.password, user.email, user.role),
                )
            return True
        except Exception as e:
            logger.exception(f"Erro ao criar usuário: {e}")
            return False

    @staticmethod
    def update_user(user: UserEntity) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute(
                    "UPDATE final_project_db.users SET username = %s, email = %s, password = %s, role = %s WHERE id = %s",
                    (user.username, user.email, user.password, user.role, user.id),
                )
            return True
        except Exception as e:
            logger.exception(f"Erro ao atualizar usuário: {e}")
            return False

    @staticmethod
    def delete_user(id: str) -> bool:
        try:
            with get_cursor() as cursor:
                cursor.execute("DELETE FROM final_project_db.users WHERE id = %s", (id,))
            return True
        except Exception as e:
            logger.exception(f"Erro ao deletar usuário: {e}")
            return False
