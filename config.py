import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")

db_config = {
    "host": os.getenv("DB_HOST", "root"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "database": DB_NAME,
    "port": int(os.getenv("DB_PORT", 3306))
}
