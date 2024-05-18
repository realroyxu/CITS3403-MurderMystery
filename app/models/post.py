from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base
from datetime import datetime

class Post(Base):
    __tablename__ = 'post'
    postid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'))
    title: Mapped[str] = mapped_column(String, nullable=False, default='(NO TITLE)')
    content: Mapped[str] = mapped_column(String, nullable=False, default='(NO CONTENT)')
    posttime: Mapped[str] = mapped_column(String, nullable=False)
    posttype: Mapped[str] = mapped_column(String, nullable=False, default='(Unknown)')
    puzzleid: Mapped[int] = mapped_column(Integer, ForeignKey('puzzle.puzzleid', ondelete='CASCADE'))
    postimage: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"Post({self.postid!r}, {self.title!r})"
