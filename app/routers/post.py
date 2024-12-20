from typing import Optional
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import func, label
from sqlmodel import select
from app import oauth2
from .. import models, schemas
from ..database import SessionDep

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=list[schemas.PostOut]) #, response_model=list[schemas.Post]
def get_posts(session: SessionDep, limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = session.exec(select(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)).all()

    result = session.exec(select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)).mappings().all()

    return result

# Only get my post
@router.get("/myposts", response_model=list[schemas.Post])
def get_posts(session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    posts = session.exec(select(models.Post).where(models.Post.owner_id == current_user.id)).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump()) 
    session.add(new_post)
    session.commit()
    session.refresh(new_post) #to get returning value last added
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    
    post = session.exec(select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id).where(models.Post.id == id)).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    post = session.get(models.Post, id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to requested action")
    
    session.delete(post)
    session.commit()

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    post = session.get(models.Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to requested action")
    
    post.sqlmodel_update(updated_post.model_dump(exclude_unset=True))
    session.add(post)  # Add the updated instance back to the session
    session.commit()  # Commit the transaction
    session.refresh(post)
    return post