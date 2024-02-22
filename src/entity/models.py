from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Integer, ForeignKey, DateTime, func, Enum, Boolean
from sqlalchemy.orm import DeclarativeBase
from datetime import date
import enum

class Base(DeclarativeBase):
    pass

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
    #tags = relationship("Tag", secondary=image_tags, backref="images")


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
    