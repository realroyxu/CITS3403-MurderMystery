import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.orm import *
from app.models.base import Base
from app.models import User, Attempt, Comment, Post, Puzzle, SiteLeaderboard, PostLeaderboard


engine = create_engine('sqlite:///ormtest.db', echo=True)


# enforce foreign key enabled, sqlite default is off
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
