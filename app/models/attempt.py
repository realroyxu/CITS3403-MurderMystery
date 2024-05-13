import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from .base import Base


class Attempt(Base):
    __tablename__ = 'attempt'
    attemptid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'))
    # attempt is no longer associated with puzzle, but with post instead
    postid: Mapped[int] = mapped_column(Integer, ForeignKey('post.postid', ondelete='CASCADE'))
    progressdata: Mapped[str] = mapped_column(String)
    # time elasped counted in seconds
    timeelapsed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Attempt({self.attemptid!r}, {self.timeelapsed!r})"
