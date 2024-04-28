create table comment
(
    commentId
        primary key,
    postId      INTEGER
        references post,
    userId      INTEGER
        references user,
    commentTime INTEGER not null,
    commentText TEXT default '(No content)'
);

