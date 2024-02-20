from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.repository import comments as reps_comments
from src.services.auth import auth_service
from src.entity.models import User, UserRole
from src.schemas.comment import CommentCreate, CommentUpdate

router = APIRouter(prefix='/comments', tags=['comments'])

@router.post("/")
async def create_comment(photo_id: int, comment: CommentCreate, db: Session = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    return await reps_comments.create_comment(db=db, user=user, photo_id=photo_id, content=comment.content)

@router.put("/{comment_id}")
async def update_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    updated_comment = await reps_comments.update_comment(db=db, comment_id=comment_id, user_id=user.id,
                                                         content=comment.content)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return updated_comment

@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, db: Session = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    if user.role == RoleEnum.ADMIN or user.role == RoleEnum.MODERATOR:
        deleted_comment = await reps_comments.delete_comment(db=db, comment_id=comment_id)
        if not deleted_comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return deleted_comment
    else:
        raise HTTPException(status_code=403, detail="Permission denied")

@router.get("/", response_model=List[CommentResponse])
async def get_all_comments(db: Session = Depends(get_db)):
    return await reps_comments.get_all_comments(db=db)

@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    comment = await reps_comments.get_comment_by_id(db=db, comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment
