import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import *
from .base import Base


class Attempt(Base):
    __tablename__ = 'attempt'
    attemptid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'))
    puzzleid: Mapped[int] = mapped_column(Integer, ForeignKey('puzzle.puzzleid', ondelete='CASCADE'))
    progressdata: Mapped[str] = mapped_column(String)
    timeelapsed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Attempt({self.attemptid!r}, {self.timeelapsed!r})"
