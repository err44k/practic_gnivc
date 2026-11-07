CREATE TABLE IF NOT EXISTS processed_receipts (
    check_id INTEGER PRIMARY KEY,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_valid BOOLEAN NOT NULL,
    validation_message TEXT NOT NULL
);