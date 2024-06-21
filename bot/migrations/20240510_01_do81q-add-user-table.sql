-- Add user table
-- depends: 

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255),
    datetime_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    balance INT DEFAULT 0
);
