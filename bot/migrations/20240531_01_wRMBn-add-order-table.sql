-- Add order table
-- depends: 20240517_01_7d2II-add-legit-table

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    client_id BIGINT,
    datetime_order TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_confirm BOOLEAN DEFAULT FALSE,
    cost INT DEFAULT 0,
    is_buy BOOLEAN DEFAULT FALSE
);