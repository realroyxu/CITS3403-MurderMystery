import sqlite3


class Database:
    def __init__(self, db_name='example.db'):
        try:
            self.conn = sqlite3.connect(db_name)
            # use row factory to return dict instead of tuple
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print("Error connecting to database: ", e)

    def execute(self, sql, data):
        try:
            cur = self.conn.cursor()
            res = cur.execute(sql, data).fetchall()
            if res:
                res = [dict(row) for row in res]
                cur.close()
                return res
            else:
                res = []
                cur.close()
                return res
        except sqlite3.Error as e:
            # using 'from e' to preserve the original traceback
            raise RuntimeError(f"{e}") from e

    def executescript(self, sql):
        # only for create table
        try:
            cur = self.conn.cursor()
            return cur.executescript(sql).fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"{e}") from e

    def commit(self):
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error committing transaction: ", e)

    def close(self):
        self.conn.close()

    def __del__(self):
        self.conn.close()


class Schema:
    def __init__(self, db):
        self.db = db

    def create_table(self):
        create_table_script = """
           CREATE TABLE IF NOT EXISTS "attempt"
           (
               attemptId INTEGER PRIMARY KEY AUTOINCREMENT ,
               puzzleId INTEGER ,
               userID INTEGER ,
               -- refers to seconds
               timeElapsed INTEGER DEFAULT 0,
               progressData TEXT,
               FOREIGN KEY (puzzleId) REFERENCES puzzle ON DELETE CASCADE,
               FOREIGN KEY (userID) REFERENCES user ON DELETE CASCADE
           );

           CREATE TABLE IF NOT EXISTS "comment" (
               commentId PRIMARY KEY AUTOINCREMENT ,
               postId INTEGER,
               userId INTEGER,
               -- calculate time based on postTime
               commentTime INTEGER NOT NULL ,
               -- likeType INTEGER,
               commentText TEXT DEFAULT '(No content)',
               FOREIGN KEY (postId) REFERENCES post ON DELETE CASCADE ,
               FOREIGN KEY (userId) REFERENCES user ON DELETE CASCADE
           );

           CREATE TABLE IF NOT EXISTS "post"
           (
               postId   INTEGER PRIMARY KEY AUTOINCREMENT,
               userId   INTEGER,
               title    TEXT DEFAULT 'NO TITLE',
               postTime TEXT NOT NULL,
               postType TEXT,
               puzzleId INTEGER,
               postText TEXT DEFAULT '(No content)',
               FOREIGN KEY (userId) REFERENCES user ON DELETE CASCADE,
               FOREIGN KEY (puzzleId) REFERENCES puzzle ON DELETE CASCADE
           );

           CREATE TABLE IF NOT EXISTS "postleaderboard"(
               recordId INTEGER PRIMARY KEY AUTOINCREMENT ,
               userId INTEGER,
               postId INTEGER,
               rank INTEGER DEFAULT 0,
               FOREIGN KEY (userId) references user ON DELETE CASCADE,
               FOREIGN KEY (postId) references post ON DELETE CASCADE
           );

           CREATE TABLE IF NOT EXISTS "puzzle"
           (
               puzzleId   INTEGER PRIMARY KEY AUTOINCREMENT,
               userId     INTEGER,
               puzzleData TEXT NOT NULL,
               createTime TEXT NOT NULL,
               category   TEXT DEFAULT 'undefined',
               FOREIGN KEY (userId) REFERENCES user ON DELETE CASCADE
           );

           CREATE TABLE IF NOT EXISTS "siteleaderboard"(
               userId INTEGER PRIMARY KEY ,
               solveCount INTEGER DEFAULT 0,
               postCount INTEGER DEFAULT 0,
               FOREIGN KEY (userId) REFERENCES user ON DELETE CASCADE
           );

           CREATE TABLE IF NOT EXISTS "user"
           (
               userId       INTEGER PRIMARY KEY AUTOINCREMENT ,
               passwordHash TEXT NOT NULL,
               email         TEXT,
               userName     TEXT NOT NULL UNIQUE,
               avatarid       INTEGER
           );

           """
        self.db.executescript(create_table_script)
        self.db.commit()


class User:
    # Data should be parsed as JSON
    def __init__(self, db):
        self.db = db

    def create_user(self, data):
        query = """
        INSERT INTO user (userName, passwordHash, email, avatarid) VALUES (:userName, :passwordHash, :email, :avatarid);
        """
        data.setdefault('avatarid', 'default.jpg')
        try:
            self.db.execute(query, data)
            self.db.commit()
            res = "User created successfully."
            return res
        except RuntimeError as e:
            raise RuntimeError(f"Error creating user: {e}") from e

    def get_user(self, data):
        # get user by userName, should be a single record
        query = """
        SELECT * FROM user WHERE userId = :userId or userName = :userName;
        """
        # test
        # query = """
        # SELECT * FROM user WHERE passwordHash = :passwordHash;
        # """
        data.setdefault('userId', None)
        try:
            res = self.db.execute(query, data)[0]
            return res

        except RuntimeError as e:
            raise RuntimeError(f"Error fetching user: {e}") from e
        # need inspecting this handler
        except IndexError:
            raise RuntimeError("Error fetching user: user not found")

    def update_user(self, data):
        query = """
        UPDATE user SET email = :email, userName = :userName, passwordHash = :passwordHash, avatarid = :avatarid
        WHERE userId = :userId;
        """
        # set default for partial update
        if 'userId' not in data:
            raise RuntimeError("Error updating user: user Not found")
        original_data = self.get_user(data)
        data.setdefault('userName', original_data['userName'])
        data.setdefault('passwordHash', original_data['passwordHash'])
        data.setdefault('email', original_data['email'])
        data.setdefault('avatarid', original_data['avatarid'])

        try:
            self.db.execute(query, data)
            self.db.commit()
            res = "User updated successfully."
            return res
        except sqlite3.Error as e:
            raise RuntimeError(f"Error updating user: {e}") from e

    def delete_user(self, data):
        query = """
        DELETE FROM user WHERE userName = :userName;
        """
        self.db.execute(query, data)
        self.db.commit()


def main():
    db = Database()
    schema = Schema(db)
    schema.create_table()

    # test
    user = User(db)
    try:
        # print(user.get_user({'passwordHash': 'foo'}))
        # print(user.get_user({'userName': 'foobar'}))
        # print(user.create_user({'userName': 'foobar3', 'passwordHash': 'foo', 'email': ''}))
        print(user.update_user({'userId': 1, 'userName': 'test123'}))
    except RuntimeError as e:
        print(e)
    db.close()


if __name__ == '__main__':
    main()
