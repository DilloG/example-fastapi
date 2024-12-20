from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..database import SessionDep
from .. import schemas, models, utils, oauth2
from sqlmodel import select
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = session.exec(select(models.User).where(models.User.email == user_credentials.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    #Create Token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    #Return Token
    return{"access_token": access_token, "token_type": "bearer"} 

#Annotated[OAuth2PasswordRequestForm, Depends()] utk ambil value form-data