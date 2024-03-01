from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Date,
    Integer,
    ForeignKey,
    DateTime,
    func,
    Enum,
    Boolean,
    Table,
    CheckConstraint,
    Column,
)
from sqlalchemy.orm import DeclarativeBase
from datetime import date
import enum
from sqlalchemy.sql.sqltypes import Date
from typing import List, Optional


class Base(DeclarativeBase):
    pass


image_association = Table(
    "image_tag_association",
    Base.metadata,
    Column("image_id", Integer, ForeignKey("images.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
    # Column("comment_id", Integer, ForeignKey("comments.id")), I commented it because comment and image has one_to_many bind
)

class GeneralAttributes(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[date] = mapped_column(
        "created_at", DateTime, default=func.now(), nullable=True
    )
    updated_at: Mapped[date] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now(), nullable=True
    )

class Tag(GeneralAttributes):
    __tablename__ = "tags"
    
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", backref="contacts", lazy="joined")

    images: Mapped[List["Image"]] = relationship(
        secondary=image_association, back_populates="tags", lazy="joined"
    )


class Image(GeneralAttributes):
    __tablename__ = "images"
    
    description: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", backref="image", lazy="joined")
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary=image_association, back_populates="images"
    )
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="image", cascade="all, delete", lazy="joined"
    )
    transformed_pics = relationship(
        "TransformedPic", back_populates="original_picture"
    )  # changed backref to back_populates


# class representing the role
class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


# Use the class for User model - representing of model User
class User(GeneralAttributes):
    __tablename__ = "users"
    
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    
    status: Mapped[bool] = mapped_column("status", Boolean, default=True)
    role: Mapped[Enum] = mapped_column(
        "role", Enum(Role), default=Role.user, nullable=True
    )
    picture_count: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )  # 2402_picture_count


class Comment(GeneralAttributes):
    __tablename__ = "comments"
    

    # photo_id: Mapped[int] = mapped_column(Integer, ForeignKey('photos.id'))#commented
    comment: Mapped[str] = mapped_column(String(255), index=True)

    
    image_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("images.id"), nullable=False
    )
    # Define relationship with User model
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", backref="comments", lazy="joined")
    # Define relationship with Photo model
    image = relationship("Image", back_populates="comments")


class TransformedPic(GeneralAttributes):
    __tablename__ = "transformed_pics"
    
    public_id: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    original_pic_id: Mapped[int] = mapped_column(ForeignKey("images.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    original_picture = relationship("Image", back_populates="transformed_pics")
