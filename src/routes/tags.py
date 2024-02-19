from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.tags import TagSchema, TagResponse
from src.repository import tags as repository_tags

router = APIRouter(prefix='/tags', tags=["tags"])


@router.get("/", response_model=List[TagResponse]) 
async def read_tags(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    """
    The read_tags function returns a list of tags.
        ---
        get:
          summary: Returns a list of tags.
          description: Get all the available tags in the database, with pagination support (skip and limit).
          responses:
            &quot;200&quot;:
              description: A JSON array containing tag objects.  Each object has an id, name, and slug field.  The id is an integer that uniquely identifies each tag in the database; it can be used to retrieve individual posts by their ID using /tags/{id}.  The name is a string that contains the human-readable
    
    :param skip: int: Skip the first n tags
    :param limit: int: Limit the number of tags returned by the function
    :param db: Session: Pass the database session to the repository layer
    :return: A list of tag objects
    :doc-author: Trelent
    """
    tags = await repository_tags.get_tags(skip, limit, db)
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
async def read_tag(tag_id: int, db: Session = Depends(get_db)):
    """
    The read_tag function returns a single tag from the database.
        The function takes in an integer as its argument, which is the ID of the tag to be returned.
        If no such tag exists, then a 404 error is raised.
    
    :param tag_id: int: Specify the id of the tag to be retrieved
    :param db: Session: Pass the database session to the function
    :return: A tag object
    :doc-author: Trelent
    """
    tag = await repository_tags.get_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.post("/", response_model=TagResponse)
async def create_tag(body: TagSchema, db: Session = Depends(get_db)):
    """
    The create_tag function creates a new tag in the database.
        The function takes a TagSchema object as input and returns the created tag.
    
    
    :param body: TagSchema: Validate the data that is passed into the function
    :param db: Session: Pass the database session to the repository layer
    :return: A tag object, which is a pydantic model
    :doc-author: Trelent
    """
    return await repository_tags.create_tag(body, db)
    


@router.delete("/{tag_id}", response_model=TagResponse)
async def remove_tag(tag_id: int, db: Session = Depends(get_db)):
    """
    The remove_tag function removes a tag from the database.
        Args:
            tag_id (int): The id of the tag to be removed.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
    
    :param tag_id: int: Specify the id of the tag to be removed
    :param db: Session: Pass the database session to the repository function
    :return: A tag object
    :doc-author: Trelent
    """
    tag = await repository_tags.remove_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag
