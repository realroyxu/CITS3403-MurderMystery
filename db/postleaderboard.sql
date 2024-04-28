create table postleaderboard
(
    recordId INTEGER
        primary key autoincrement,
    userId   INTEGER
        references user,
    postId   INTEGER
        references post,
    rank     INTEGER default 0
);

