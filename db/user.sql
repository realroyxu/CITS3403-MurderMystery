create table user
(
    userId       INTEGER
        primary key,
    passwordHash TEXT not null,
    mail         TEXT,
    userName     TEXT not null
        unique,
    avatar       TEXT
);

