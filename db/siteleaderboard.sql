create table siteleaderboard
(
    userId     INTEGER
        primary key
        references user,
    solveCount INTEGER default 0,
    postCount  INTEGER default 0
);

