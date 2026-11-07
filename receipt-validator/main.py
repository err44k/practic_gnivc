import json
from kafka import KafkaConsumer

from database import is_receipt_processed, save_processing_result

consumer = KafkaConsumer(
    "receipts-topic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="receipt-validator-group",
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

print("Receipt Validator запущен. Ожидаю чеки...")

def validate_receipt(receipt):
    required_fields = [
        "check_id",
        "created_at",
        "items",
        "check_sum"
    ]

    for field in required_fields:
        if field not in receipt:
            return False, f"Отсутствует поле: {field}"

    if not isinstance(receipt["check_id"], int):
        return False, "check_id должен быть целым числом"

    if not isinstance(receipt["created_at"], str):
        return False, "created_at должен быть строкой"

    if not isinstance(receipt["items"], list):
        return False, "items должен быть списком"

    if not isinstance(receipt["check_sum"], (int, float)):
        return False, "check_sum должен быть числом"

    

    for item in receipt["items"]:

        required_item_fields = [
            "item_name",
            "item_price",
            "item_type",
            "item_quantity",
            "item_sum"
        ]

        for field in required_item_fields:
            if field not in item:
                return False, f"В товаре отсутствует поле: {field}"

        if not isinstance(item["item_name"], str):
            return False, "Название товара должно быть строкой"

        if not isinstance(item["item_price"], (int, float)):
            return False, "Цена товара должна быть числом"

        if not isinstance(item["item_type"], int):
            return False, "Тип товара должен быть целым числом"

        if not isinstance(item["item_quantity"], (int, float)):
            return False, "Количество товара должно быть числом"

        if not isinstance(item["item_sum"], (int, float)):
            return False, "Сумма товара должна быть числом"

        
        if item["item_price"] <= 0:
            return False, "Цена товара должна быть больше нуля"

        if item["item_quantity"] <= 0:
            return False, "Количество товара должно быть больше нуля"

        if item["item_sum"] < 0:
            return False, "Сумма товара не может быть отрицательной"


        expected_sum = round(
            item["item_price"] * item["item_quantity"],
            2
        )

        if abs(item["item_sum"] - expected_sum) > 0.01:
            return False, (
                f"Неверная сумма товара {item['item_name']}: "
                f"ожидалось {expected_sum}, "
                f"получено {item['item_sum']}"
            )


    expected_check_sum = round(
        sum(item["item_sum"] for item in receipt["items"]),
        2
    )

    if abs(receipt["check_sum"] - expected_check_sum) > 0.01:
        return False, (
            f"Неверная сумма чека: "
            f"ожидалось {expected_check_sum}, "
            f"получено {receipt['check_sum']}"
        )


    return True, "Чек прошёл все проверки"

    

for message in consumer:
    receipt = message.value
    check_id = receipt.get("check_id")

    print(f"\nПолучен чек: {check_id if check_id is not None else 'неизвестен'}")

    if isinstance(check_id, int) and is_receipt_processed(check_id):
        print(f"❌ Дубликат чека: {check_id}")
        continue

    is_valid, message_text = validate_receipt(receipt)

    if isinstance(check_id, int) and not isinstance(check_id, bool):
        save_processing_result(check_id, is_valid, message_text)

    if is_valid:
        print(f"✅ Валидный чек: {message_text}")
    else:
        print(f"❌ Невалидный чек: {message_text}")