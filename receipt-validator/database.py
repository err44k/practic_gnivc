import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def is_receipt_processed(check_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM processed_receipts
                    WHERE check_id = %s
                )
                """,
                (check_id,)
            )
            return cursor.fetchone()[0]


def save_processing_result(check_id, is_valid, message):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO processed_receipts
                    (check_id, is_valid, validation_message)
                VALUES (%s, %s, %s)
                """,
                (check_id, is_valid, message)
            )