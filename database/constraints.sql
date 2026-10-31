ALTER TABLE checks
ADD CONSTRAINT checks_sum_positive
CHECK (check_sum >= 0);

ALTER TABLE items
ADD CONSTRAINT items_price_positive
CHECK (item_price > 0);

ALTER TABLE items
ADD CONSTRAINT items_quantity_positive
CHECK (item_quantity > 0);

ALTER TABLE items
ADD CONSTRAINT items_sum_non_negative
CHECK (item_sum >= 0);