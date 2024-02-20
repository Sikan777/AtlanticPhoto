from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import String, Integer, CheckConstraint, ForeignKey, DateTime, func, Boolean, Enum, Table, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.sqltypes import Date
from datetime import date
from typing import List, Optional


from sqlalchemy import String, Date, Integer, ForeignKey, DateTime, func, Enum, Boolean
from sqlalchemy.orm import DeclarativeBase
from datetime import date
import enum


class Base(DeclarativeBase):
    pass

picture_tag_association = Table(
    'picture_tag_association',
    Base.metadata,
    Column('picture_id', Integer, ForeignKey('pictures.id', ondelete="CASCADE")),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    
    created_at: Mapped[date] = mapped_column(
        'created_at', DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[date] = mapped_column(
        'updated_at', DateTime, default=func.now(), onupdate=func.now(), nullable=True)

    #Ждем pictures
    #pictures: Mapped[List["Picture"]] = relationship(secondary=picture_tag_association, back_populates='tags', lazy='joined')

# class representing the role
class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"

# Use the class for User model - representing of model User
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    status: Mapped[bool] = mapped_column('status', Boolean, default=True)
    role: Mapped[Enum] = mapped_column('role', Enum(Role), default=Role.user, nullable=True)
    

