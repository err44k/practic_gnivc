import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(
        value,
        ensure_ascii=False
    ).encode("utf-8")
)

invalid_receipt = {
    "check_id": 901314,
    "created_at": "2026-11-01T12:00:00+00:00",
    "org_id": 1,
    "items": [
        {
            "item_name": "Молоко",
            "item_price": 420.00,
            "item_type": 1,
            "item_quantity": 5,
            "item_sum": 2100.00
        }
    ],
    "check_sum": 2100.00
}

future = producer.send("receipts-topic", invalid_receipt)
metadata = future.get(timeout=10)

print(
    f"Тестовый чек отправлен: {invalid_receipt['check_id']}, "
    f"топик: {metadata.topic}"
)

producer.close()