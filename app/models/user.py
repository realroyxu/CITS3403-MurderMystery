from sqlalchemy import Column, Integer, String
from sqlalchemy import *
from sqlalchemy.orm import *
from app.models.base import Base


class User(Base):
    __tablename__ = 'user'
    # userid is managed by db, as "autoincrement=True"
    userid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=True)
    avatar: Mapped[str] = mapped_column(String, nullable=True)
