from database import get_connection

try:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM processed_receipts")
            result = cursor.fetchone()

            print("Подключение успешно!")
            print("Количество обработанных чеков:", result[0])

except Exception as error:
    print("Ошибка подключения к базе:", error)