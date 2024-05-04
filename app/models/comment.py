from sqlalchemy import Column, Integer, String
from sqlalchemy import *
from sqlalchemy.orm import *
from app.models.base import Base


class Comment(Base):
    __tablename__ = 'comment'
    commentid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'))
    postid: Mapped[int] = mapped_column(Integer, ForeignKey('post.postid', ondelete='CASCADE'))
    commenttext: Mapped[str] = mapped_column(String, default='(NO CONTENT)')
    commenttime: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"Comment({self.commentid!r}, {self.commenttext!r})"
