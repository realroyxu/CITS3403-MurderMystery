from sqlalchemy import create_engine, Engine, event
from sqlalchemy.orm import sessionmaker
from app.models.base import Base

# these import are NEEDED WTF
from app.models.comment import Comment
from app.models.failure import Failure
from app.models.post import Post
from app.models.puzzle import Puzzle
from app.models.user import User
from app.models.attempt import Attempt
from app.models.siteleaderboard import SiteLeaderboard
from app.models.postleaderboard import PostLeaderboard

# relative path and current file tree structure could be a problem
engine = create_engine('sqlite:///db/ormtest.db', echo=True)


# enforce foreign key enabled, sqlite default is off
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
