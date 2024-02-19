from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, CheckConstraint, ForeignKey, DateTime, func, Boolean, Enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.sqltypes import Date
from datetime import date


class Base(DeclarativeBase):
    pass


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now(),
                                             nullable=True)

    #user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    #user: Mapped["User"] = relationship("User", backref="contacts", lazy="joined")