import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE, override=True)

print("Загружен файл:", ENV_FILE)
print("DB_HOST:", repr(os.getenv("DB_HOST")))
print("DB_PORT:", repr(os.getenv("DB_PORT")))
print("DB_NAME:", repr(os.getenv("DB_NAME")))
print("DB_USER:", repr(os.getenv("DB_USER")))
print("Пароль загружен:", bool(os.getenv("DB_PASSWORD")))

with psycopg.connect(
    host="127.0.0.1",
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
) as connection:
    print("\nУспешное подключение к PostgreSQL!")

    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        print(cursor.fetchone()[0])