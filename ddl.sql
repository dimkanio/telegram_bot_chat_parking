-- Таблица: cars
DROP TABLE IF EXISTS cars;
CREATE TABLE cars (
        id SERIAL PRIMARY KEY,
        tg_user_id BIGINT NOT NULL,
        car_number VARCHAR (20),
        model VARCHAR,
        UNIQUE (tg_user_id, car_number)
);

-- Таблица: contacts
DROP TABLE IF EXISTS contacts;
CREATE TABLE contacts (
        id SERIAL PRIMARY KEY,
        tg_user_id BIGINT NOT NULL,
        phone VARCHAR (20),
        UNIQUE (tg_user_id, phone)
);

-- Таблица: messages
DROP TABLE IF EXISTS messages;
CREATE TABLE messages (
        id SERIAL PRIMARY KEY,
        from_tg_user_id BIGINT NOT NULL,
        to_tg_user_id BIGINT,
        hex_dig VARCHAR,
        chat_type VARCHAR,
        dialog_state VARCHAR,
        message TEXT,
        UNIQUE (hex_dig)
);

-- Таблица: park_mm
DROP TABLE IF EXISTS park_mm;
CREATE TABLE park_mm (
        id SERIAL PRIMARY KEY,
        tg_user_id BIGINT NOT NULL,
        park_mm INT,
        rent VARCHAR, 
        UNIQUE (tg_user_id, park_mm)
);

-- Таблица: users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        tg_user_id BIGINT NOT NULL,
        first_name VARCHAR (40),
        last_name VARCHAR (40),
        is_in_chat BOOLEAN DEFAULT FALSE,
        tg_mention VARCHAR (100),
        tg_chat_id BIGINT ,
        UNIQUE (tg_user_id)
);

-- Таблица: html
DROP TABLE IF EXISTS html;
CREATE TABLE html (
        num BIGINT ,
        page_html TEXT,
        date_added VARCHAR(40) default NULL,
        UNIQUE (num)
);