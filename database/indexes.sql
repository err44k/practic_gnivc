CREATE INDEX idx_checks_created_at
ON checks(created_at);

CREATE INDEX idx_checks_user_id
ON checks(user_id);

CREATE INDEX idx_checks_org_id
ON checks(org_id);

CREATE INDEX idx_items_check_id
ON items(check_id);