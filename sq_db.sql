CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    is_admin integer DEFAULT 0,
    time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS requests (
    id integer PRIMARY KEY AUTOINCREMENT,
    user_id text NOT NULL,
    friend_id text NOT NULL,
    user_name text NOT NULL,
    time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS couples (
    id integer PRIMARY KEY AUTOINCREMENT,
    user1 text NOT NULL,
    user2 text NOT NULL,
    name1 text NOT NULL,
    name2 text NOT NULL,
    task_to1 text NOT NULL DEFAULT "Заданий нет",
    task_to2 text NOT NULL DEFAULT "Заданий нет",
    time integer NOT NULL
);