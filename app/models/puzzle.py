from sqlalchemy import Column, Integer, String
from sqlalchemy import *
from sqlalchemy.orm import *
from app.models.base import Base


class Puzzle(Base):
    __tablename__ = 'puzzle'
    puzzleid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'))
    puzzledata: Mapped[str] = mapped_column(String, nullable=False)
    createtime: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, default='undefined')

    def __repr__(self):
        return f"Puzzle({self.puzzleid!r}, {self.category!r})"
