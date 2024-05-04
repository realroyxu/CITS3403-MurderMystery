from sqlalchemy import Column, Integer, String
from sqlalchemy import *
from sqlalchemy.orm import *
from app.models.base import Base


class PostLeaderboard(Base):
    __tablename__ = 'postleaderboard'
    recordid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'))
    postid: Mapped[int] = mapped_column(Integer, ForeignKey('post.postid', ondelete='CASCADE'))
    rank: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"PostLeaderboard({self.recordid!r}, {self.rank!r})"
