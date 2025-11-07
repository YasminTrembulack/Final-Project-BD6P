from uuid import uuid4
from loguru import logger
from contextlib import contextmanager
from datetime import datetime, timezone
from dataclasses import dataclass, field
from mysql.connector import connect, Error

from config import db_config

@dataclass(kw_only=True)
class BaseEntity:
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@contextmanager
def get_cursor(dictionary: bool = True):
    conn = None
    cursor = None
    try:
        conn = connect(**db_config)
        cursor = conn.cursor(dictionary=dictionary)
        yield cursor
        conn.commit()
    except Error as e:
        logger.exception(f"Erro ao conectar no banco: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
