-- Add find table
-- depends: 20240510_01_do81q-add-user-table

CREATE TABLE finds (
    id SERIAL PRIMARY KEY,
    client_id BIGINT,
    datetime_order TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cost INT,
    is_confirm BOOLEAN DEFAULT FALSE,
    datetime_confirmed TIMESTAMP
);