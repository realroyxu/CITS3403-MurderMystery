from sqlalchemy import Column, Integer, String
from sqlalchemy import *
from sqlalchemy.orm import *
from app.models.base import Base


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
