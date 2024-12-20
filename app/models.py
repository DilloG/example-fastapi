from typing import ClassVar
from sqlmodel import Field, SQLModel
from sqlalchemy import text
from sqlalchemy.orm import relationship
from datetime import datetime

class Post(SQLModel, table=True):
    __tablename__ = "post"
    __table_args__ = {'mysql_engine':'InnoDB'}

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str = Field(index=True)
    published: int = Field(default=1, index=True)
    created_at: datetime = Field(sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")})
    owner_id: int = Field(foreign_key="user.id", ondelete="CASCADE")

    owner: ClassVar['User'] = relationship('User')
 
class User(SQLModel, table=True):
    __tablename__ = "user"
    __table_args__ = {'mysql_engine':'InnoDB'}

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password: str = Field()
    created_at: datetime = Field(sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")})
    phone_number: str | None = Field(default=None)

class Vote(SQLModel, table=True):
    __tablename__ = 'vote'
    __table_args__ = {'mysql_engine':'InnoDB'}

    user_id : int = Field(foreign_key="user.id", ondelete="CASCADE", primary_key=True)
    post_id : int = Field(foreign_key="post.id", ondelete="CASCADE", primary_key=True)
