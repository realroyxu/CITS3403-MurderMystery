create table attempt
(
    attemptId    INTEGER
        primary key autoincrement,
    puzzleId     INTEGER
        references puzzle,
    userID       INTEGER
        references user,
    timeElapsed  INTEGER default 0,
    progressData TEXT
);

