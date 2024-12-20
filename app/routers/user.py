from fastapi import Depends, HTTPException, status, APIRouter
from sqlmodel import select

from app import oauth2
from .. import models, schemas, utils
from ..database import SessionDep

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, session: SessionDep, user_id: int = Depends(oauth2.get_current_user)):

    #Hash Password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump()) 
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, session: SessionDep, user_id: int = Depends(oauth2.get_current_user)):
    user = session.exec(select(models.User).where(models.User.id == id)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User id {id} not found")

    return user
