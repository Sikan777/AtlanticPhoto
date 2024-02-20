from sqlalchemy.orm import Session
from src.entity.models import Comment
from src.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from datetime import datetime
from typing import List
from src.entity.models import UserRole

def create_comment(db: Session, photo_id: int, comment: CommentCreate):
    db_comment = Comment(photo_id=photo_id, content=comment.content)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


async def update_comment(db: Session, comment_id: int, user_id: int, content: str):
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user_id).first()
    if comment:
        if not content.strip():  # Перевірка чи не лишається пробіли
            return None
        comment.content = content
        comment.updated_at = datetime.utcnow()
        db.commit()
        return comment
    return None

def delete_comment(db: Session, comment_id: int, user_role: UserRole):
    if user_role in [UserRole.ADMIN, UserRole.MODERATOR]:
        db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if db_comment:
            db.delete(db_comment)
            db.commit()
        return db_comment
    else:
        raise ValueError("User doesn't have permission to delete comment")

def get_all_comments(db: Session) -> List[CommentResponse]:
    return db.query(Comment).all()

def get_comment_by_id(db: Session, comment_id: int) -> CommentResponse:
    return db.query(Comment).filter(Comment.id == comment_id).first()
