from sqlalchemy import Column, Integer, String
from sqlalchemy import *
from sqlalchemy.orm import *
from app.models.base import Base

class SiteLeaderboard(Base):
    __tablename__ = 'siteleaderboard'
    userid: Mapped[int] = mapped_column(Integer, ForeignKey('user.userid', ondelete='CASCADE'), primary_key=True)
    solvecount: Mapped[int] = mapped_column(Integer, default=0)
    postcount: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"SiteLeaderboard({self.userid!r}, {self.solvecount!r})"
