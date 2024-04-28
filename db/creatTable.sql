CREATE TABLE "attempt"
(
    attemptId INTEGER PRIMARY KEY AUTOINCREMENT ,
    puzzleId INTEGER ,
    userID INTEGER ,
    -- refers to seconds
    timeElapsed INTEGER DEFAULT 0,
    progressData TEXT,
    FOREIGN KEY (puzzleId) REFERENCES puzzle,
    FOREIGN KEY (userID) REFERENCES user
)

CREATE TABLE "comment" (
    commentId PRIMARY KEY ,
    postId INTEGER,
    userId INTEGER,
    -- calculate time based on postTime
    commentTime INTEGER NOT NULL ,
    -- likeType INTEGER,
    commentText TEXT DEFAULT '(No content)',
    FOREIGN KEY (postId) REFERENCES post,
    FOREIGN KEY (userId) REFERENCES user
)

CREATE TABLE "post"
(
    postId   INTEGER PRIMARY KEY AUTOINCREMENT,
    userId   INTEGER,
    title    TEXT DEFAULT 'NO TITLE',
    postTime TEXT NOT NULL,
    postType TEXT,
    puzzleId INTEGER,
    postText TEXT DEFAULT '(No content)',
    FOREIGN KEY (userId) REFERENCES user,
    FOREIGN KEY (puzzleId) REFERENCES puzzle
)

CREATE TABLE "postleaderboard"(
    recordId INTEGER PRIMARY KEY AUTOINCREMENT ,
    userId INTEGER,
    postId INTEGER,
    rank INTEGER DEFAULT 0,
    FOREIGN KEY (userId) references user,
    FOREIGN KEY (postId) references post
)

CREATE TABLE "puzzle"
(
    puzzleId   INTEGER PRIMARY KEY AUTOINCREMENT,
    userId     INTEGER,
    puzzleData TEXT NOT NULL,
    createTime TEXT NOT NULL,
    category   TEXT DEFAULT 'undefined',
    FOREIGN KEY (userId) REFERENCES user
)

CREATE TABLE "siteleaderboard"(
    userId INTEGER PRIMARY KEY ,
    solveCount INTEGER DEFAULT 0,
    postCount INTEGER DEFAULT 0,
    FOREIGN KEY (userId) REFERENCES user
)

CREATE TABLE sqlite_sequence(name,seq)

CREATE TABLE "user"
(
    userId       INTEGER PRIMARY KEY,
    passwordHash TEXT NOT NULL,
    mail         TEXT,
    userName     TEXT NOT NULL UNIQUE,
    avatar       TEXT
)


