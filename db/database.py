import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from app.models.base import Base
from app.models import User, Attempt, Comment, Post, Puzzle, SiteLeaderboard, PostLeaderboard

engine = create_engine('sqlite:///ormtest.db', echo=True)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
