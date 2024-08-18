CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS requests (
    id integer PRIMARY KEY AUTOINCREMENT,
    user_id text NOT NULL,
    friend_id text NOT NULL,
    time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS couples (
    id integer PRIMARY KEY AUTOINCREMENT,
    user1 text NOT NULL,
    user2 text NOT NULL,
    time integer NOT NULL
);