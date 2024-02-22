from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Integer, ForeignKey, DateTime, func, Enum, Boolean, Table, CheckConstraint, Column
from sqlalchemy.orm import DeclarativeBase
from datetime import date
import enum
from sqlalchemy.sql.sqltypes import Date
from typing import List, Optional


class Base(DeclarativeBase):
    pass


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    created_at: Mapped[date] = mapped_column(
        'created_at', DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[date] = mapped_column(
        'updated_at', DateTime, default=func.now(), onupdate=func.now(), nullable=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    user: Mapped["User"] = relationship("User", backref="contacts", lazy="joined")

    # Ждем pictures
    # pictures: Mapped[List["Picture"]] = relationship(secondary=picture_tag_association, back_populates='tags', lazy='joined')


class Image(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now(),
                                             nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    user: Mapped["User"] = relationship("User", backref="todos", lazy="joined")
    # tags = relationship("Tag", secondary=image_tags, backref="images")


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


class Comment(Base):
    tablename = 'comments'
    id: Mapped[int] = mapped_column(primary_key=True)

    # photo_id: Mapped[int] = mapped_column(Integer, ForeignKey('photos.id'))#commented
    comment: Mapped[str] = mapped_column(String(255), index=True)

    created_at: Mapped[date] = mapped_column(
        'created_at', DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[date] = mapped_column(
        'updated_at', DateTime, default=func.now(), onupdate=func.now(), nullable=True)

    # Define relationship with User model
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped["User"] = relationship("User", backref="comments", lazy="joined")
    # Define relationship with Photo model
    # photo = relationship("Photo", back_populates="comments")

class TransformedPic(Base):
    __tablename__ = "transformed_pics"
    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    # original_pic_id: Mapped[int] = mapped_column(
    #    ForeignKey("images.id"), nullable=False
    # )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[date] = mapped_column(
        "created_at", DateTime, default=func.now(), nullable=True
    )
    updated_at: Mapped[date] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now()
    )
    # original_picture = relationship("Image", back_populates="transformed_pictures")