import json
import random
from pathlib import Path
from datetime import datetime, timezone
from kafka import KafkaProducer

BASE_DIR = Path(__file__).resolve().parent

PRODUCTS_FILE = BASE_DIR / "data" / "products.json"
ORGANIZATIONS_FILE = BASE_DIR / "data" / "organizations.json"

with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
    products = json.load(file)

with open(ORGANIZATIONS_FILE, "r", encoding="utf-8") as file:
    organizations = json.load(file)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(
        value,
        ensure_ascii=False
    ).encode("utf-8")
)

def generate_receipt():
    organization = random.choice(organizations)

    items_count = random.randint(1, len(products))
    selected_products = random.sample(products, items_count)

    receipt_items = []

    for product in selected_products:
        quantity = random.randint(1, 5)
        item_sum = round(product["item_price"] * quantity, 2)

        receipt_items.append({
            "item_name": product["item_name"],
            "item_price": product["item_price"],
            "item_type": product["item_type"],
            "item_quantity": quantity,
            "item_sum": item_sum
        })

    check_sum = round(sum(item["item_sum"] for item in receipt_items), 2)

    receipt = {
        "check_id": random.randint(100000, 999999),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "org_id": organization["org_id"],
        "items": receipt_items,
        "check_sum": check_sum
    }

    return receipt


receipt = generate_receipt()

future = producer.send("receipts-topic", receipt)

metadata = future.get(timeout=10)

print(
    f"Чек {receipt['check_id']} отправлен в Kafka. "
    f"Топик: {metadata.topic}, партиция: {metadata.partition}"
)

producer.close()