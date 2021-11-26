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
                          to_mm INT,
                          to_car VARCHAR,
                          to_phone VARCHAR,
                          message TEXT
);

-- Таблица: park_mm
DROP TABLE IF EXISTS park_mm;
CREATE TABLE park_mm (
                         id SERIAL PRIMARY KEY,
                         tg_user_id BIGINT NOT NULL,
                         park_mm INT,
                         rent VARCHAR, UNIQUE (tg_user_id, park_mm)
);

-- Таблица: users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
                       id SERIAL PRIMARY KEY,
                       tg_user_id BIGINT UNIQUE NOT NULL,
                       first_name VARCHAR (40),
                       last_name VARCHAR (40),
                       is_in_chat BOOLEAN DEFAULT FALSE,
                       tg_mention VARCHAR (100)
);

