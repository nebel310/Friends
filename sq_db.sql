CREATE TABLE IF NOT EXISTS Users (
    id integer PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
);