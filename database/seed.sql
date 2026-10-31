BEGIN;

INSERT INTO users (user_id)
VALUES (1);

INSERT INTO organizations (org_id, org_name, legal_form)
VALUES (1, 'ООО Ромашка', 'ООО');

INSERT INTO checks (
    check_id,
    created_at,
    check_sum,
    user_id,
    org_id,
    invoice_id
)
VALUES (
    1001,
    NOW(),
    1130.00,
    1,
    1,
    5001
);

INSERT INTO items (
    item_name,
    item_price,
    item_type,
    item_quantity,
    item_sum,
    check_id
)
VALUES
    ('Молоко', 420.00, 1, 2.000, 840.00, 1001),
    ('Хлеб', 290.00, 2, 1.000, 290.00, 1001);

COMMIT;