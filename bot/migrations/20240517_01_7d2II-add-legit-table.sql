-- add_legit_table
-- depends: 20240511_01_gam1z-add-find-table

CREATE TABLE legits (
    id SERIAL PRIMARY KEY,
    client_id BIGINT,
    datetime_order TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cost INT,
    is_confirm BOOLEAN DEFAULT FALSE,
    decision BOOLEAN,
    datetime_confirmed TIMESTAMP
);