create table puzzle
(
    puzzleId   INTEGER
        primary key autoincrement,
    userId     INTEGER
        references user,
    puzzleData TEXT not null,
    createTime TEXT not null,
    category   TEXT default 'undefined'
);

