create table post
(
    postId   INTEGER
        primary key autoincrement,
    userId   INTEGER
        references user,
    title    TEXT default 'NO TITLE',
    postTime TEXT not null,
    postType TEXT,
    puzzleId INTEGER
        references puzzle,
    postText TEXT default '(No content)'
);

