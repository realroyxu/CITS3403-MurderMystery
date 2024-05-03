import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *

engine = create_engine('sqlite:///ormtest.db', echo=True)

# test
with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    userid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String ,nullable=True)
    avatar: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"User({self.userid!r}, {self.username!r})"

    @classmethod
    def get_id(cls, data):
        if 'username' not in data:
            raise RuntimeError("Error updating user: username not provided.")
        with Session() as s:
            try:
                stmt = select(cls.userid).where(cls.username == data['username'])
                return s.execute(stmt).one()
            except sqlalchemy.exc.NoResultFound:
                raise RuntimeError("Error fetching user: No user found.")
        # need error hanlding

    @classmethod
    def get_all(cls, data):
        if 'userid' not in data:
            raise RuntimeError("Error updating user: userid not provided.")
        with Session() as s:
            stmt = select(cls.userid, cls.username, cls.email, cls.avatar).where(cls.userid == data['userid'])
            try:
                res = s.execute(stmt).one()
                if res:
                    # _asdict() is a dict-ize method of RowProxy
                    return res._asdict()
            except sqlalchemy.exc.NoResultFound:
                raise RuntimeError("Error fetching user: No user found.")

    @classmethod
    def add_user(cls, data):
        if 'username' not in data:
            raise RuntimeError("Error updating user: username not provided.")
        if 'password' not in data:
            raise RuntimeError("Error updating user: password not provided.")
        for item in data.keys():
            if item not in ('username', 'password', 'email', 'avatar'):
                raise RuntimeError("Error updating user: invalid field provided.")
        with Session() as s:
            try:
                user = cls(**data)
                s.add(user)
                s.commit()
            except sqlalchemy.exc.IntegrityError as e:
                raise RuntimeError(f"Error adding user: integrity violated. {e}") from e

    @classmethod
    def update_user(cls, data):
        if 'userid' not in data:
            raise RuntimeError("Error updating user: userid not provided.")
        with Session() as s:
            try:
                stmt = select(cls).where(cls.userid == data['userid'])
                # return a instance, update op will be done on this instance has to be scalar() instead of one(),
                # because scalar() returns: <class '__main__.User'> and one() returns:<class
                # 'sqlalchemy.engine.row.Row'>
                user = s.execute(stmt).scalar_one()
                user.username = data.get('username', user.username)
                user.email = data.get('email', user.email)
                user.avatar = data.get('avatar', user.avatar)
                s.commit()
                return "User updated successfully."
            except sqlalchemy.exc.NoResultFound:
                raise RuntimeError("Error updating user: No user found.")

    @classmethod
    def delete_user(cls, data):
        if 'userid' not in data:
            raise RuntimeError("Error updating user: userid not provided.")
        with Session() as s:
            try:
                stmt = select(cls).where(cls.userid == data['userid'])
                user = s.execute(stmt).scalar_one()
                s.delete(user)
                s.commit()
            except sqlalchemy.exc.NoResultFound:
                raise RuntimeError("Error updating user: No user found.")
        return "User deleted successfully."


class Post(Base):
    __tablename__ = 'post'
    postid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'))
    title: Mapped[str] = mapped_column(String, nullable=False, default='(NO TITLE)')
    content: Mapped[str] = mapped_column(String, nullable=False, default='(NO CONTENT)')
    posttime: Mapped[str] = mapped_column(String, nullable=False)
    posttype: Mapped[str] = mapped_column(String)
    puzzleid: Mapped[int] = mapped_column(Integer, ForeignKey('puzzle.puzzleid', ondelete='CASCADE'))

    def __repr__(self):
        return f"Post({self.postid!r}, {self.title!r})"


class Puzzle(Base):
    __tablename__ = 'puzzle'
    puzzleid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'))
    puzzledata: Mapped[str] = mapped_column(String, nullable=False)
    createtime: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, default='undefined')

    def __repr__(self):
        return f"Puzzle({self.puzzleid!r}, {self.category!r})"


class PostLeaderboard(Base):
    __tablename__ = 'postleaderboard'
    recordid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'))
    postid: Mapped[int] = mapped_column(Integer, ForeignKey('post.postid', ondelete='CASCADE'))
    rank: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"PostLeaderboard({self.recordid!r}, {self.rank!r})"


class SiteLeaderboard(Base):
    __tablename__ = 'siteleaderboard'
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'), primary_key=True)
    solvecount: Mapped[int] = mapped_column(Integer, default=0)
    postcount: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"SiteLeaderboard({self.userid!r}, {self.solvecount!r})"


class Attempt(Base):
    __tablename__ = 'attempt'
    attemptid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'))
    puzzleid: Mapped[int] = mapped_column(Integer, ForeignKey('puzzle.puzzleid', ondelete='CASCADE'))
    progressdata: Mapped[str] = mapped_column(String)
    timeelapsed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Attempt({self.attemptid!r}, {self.timeelapsed!r})"


class Comment(Base):
    __tablename__ = 'comment'
    commentid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'))
    postid: Mapped[int] = mapped_column(Integer, ForeignKey('post.postid', ondelete='CASCADE'))
    commenttext: Mapped[str] = mapped_column(String, default='(NO CONTENT)')
    commenttime: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"Comment({self.commentid!r}, {self.commenttext!r})"


Base.metadata.create_all(engine)
try:
    print(User.add_user({'username': 'newname12', 'password': '123456'}))
    # print(User.get_all(11))
    # print(User.update_user({'username': 'newnameA', 'userid': 1}))
    # print(User.delete_user({'userid': 1}))
except Exception as e:
    print(e)
# print(User.update_user({'username': 'newname', 'userid': 11}))
