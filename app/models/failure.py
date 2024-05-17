from sqlalchemy import *
from sqlalchemy.orm import *
from app.models.base import Base


class Failure(Base):
    __tablename__ = 'failure'
    failureid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'))
    postid: Mapped[int] = mapped_column(Integer, ForeignKey('post.postid', ondelete='CASCADE'))

    def __repr__(self):
        return f"Failure({self.failureid!r}, {self.userid!r}, {self.postid!r})"
