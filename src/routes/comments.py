from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.services.auth import auth_service
from src.database.db import get_db
from src.entity.models import User, Role
from src.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from src.repository import comments as repository_comments


router = APIRouter(prefix='/comments', tags=['comments'])

@router.post("/", response_model=CommentResponse)
async def create_comment(
    photo_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user)
):
    return await repository_comments.create_comment(db=db, photo_id=photo_id, comment=comment, user_id=user.id)

@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user)
):
    updated_comment = await repository_comments.update_comment(db=db, comment_id=comment_id,
                                                               user_id=user.id, content=comment.content)
    if not updated_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return updated_comment

@router.delete("/{comment_id}", response_model=CommentResponse)
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user)
):
    if user.role in [Role.admin, Role.moderator]:
        deleted_comment = await repository_comments.delete_comment(db=db, comment_id=comment_id)
        if not deleted_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        return deleted_comment
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

@router.get("/", response_model=List[CommentResponse])
async def get_all_comments(
    db: Session = Depends(get_db)
):
    return await repository_comments.get_all_comments(db=db)

@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment_by_id(
    comment_id: int,
    db: Session = Depends(get_db)
):
    comment = await repository_comments.get_comment_by_id(db=db, comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment
