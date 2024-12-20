from fastapi import FastAPI
from sqlmodel import SQLModel
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup") 
# def on_startup():
#     create_db_and_tables()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"messsage": "Hello world!"}



# @app.get("/heroes/")
# def read_heroes(
#     session: SessionDep,
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,
# ) -> list[Hero]:
#     heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
#     return heroes

# @app.post("/heroes/")
# def create_hero(hero: Hero, session: SessionDep) -> Hero:
#     session.add(hero)
#     session.commit()
#     session.refresh(hero)
#     return hero





# @app.get("/heroes/{hero_id}")
# def read_hero(hero_id: int, session: SessionDep) -> Hero:
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     return hero


# @app.delete("/heroes/{hero_id}")
# def delete_hero(hero_id: int, session: SessionDep):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(hero)
#     session.commit()
#     return {"ok": True}


# from typing import Optional
# from fastapi import FastAPI, Body, Response, status, HTTPException
# from pydantic import BaseModel
# from random import randrange
# from databases import Database
# from sqlalchemy import create_engine, MetaData
# import asyncio
# import aiomysql
# import time

# app = FastAPI()

# #Testing conn
# async def test_example(loop):
#     conn = await aiomysql.connect(host='127.0.0.1', port=3306,
#                                   user='root', password='', db='fastapi',
#                                   loop=loop)

#     async with conn.cursor() as cur:
#         await cur.execute("SELECT * FROM products")
#         print(cur.description)
#         r = await cur.fetchall()
#         print(r)
#     conn.close()


# loop = asyncio.get_event_loop()
# loop.create_task(test_example(loop))


# # Database connection configuration
# async def get_db_connection():
#     conn = await aiomysql.connect(
#         host='127.0.0.1', port=3306,
#         user='root', password='', db='fastapi'
#     )
#     return conn

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = 1
#     rating: Optional[int] = None


# @app.get("/") #decorator
# def root():
#     return {"message": "Hello World!!"}

# # FastAPI route to fetch posts from database
# @app.get("/posts")
# async def get_posts():
#     conn = None
#     try:
#         # Establish database connection
#         conn = await get_db_connection()
#         async with conn.cursor(aiomysql.DictCursor) as cursor:
#             await cursor.execute("SELECT * FROM posts")
#             result = await cursor.fetchall()
#         return {"data": result}
    
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
#     finally:
#         # Ensure the database connection is closed
#         if conn:
#             conn.close()


# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# async def create_posts(post: Post):
#     try:
#         # Establish database connection
#         conn = await get_db_connection()
#         async with conn.cursor(aiomysql.DictCursor) as cursor:
#             # Insert new post into the database
#             await cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)", (post.title, post.content, post.published))
#             new_post_id = cursor.lastrowid
            
#             # Fetch the newly inserted post
#             await cursor.execute("SELECT * FROM posts WHERE id = %s", (new_post_id,))
#             new_post = await cursor.fetchone()
            
#             # Check if post was successfully retrieved
#             if not new_post:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found after creation")

#             return {"data": new_post}
        
#     except Exception as e:
#         # Handle any unexpected errors and log them
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
#     finally:
#         # Ensure the database connection is closed
#         if conn:
#             conn.close()

        
# @app.get("/posts/{id}")
# async def get_posts(id: int, response: Response):
#     conn = await get_db_connection()
#     async with conn.cursor(aiomysql.DictCursor) as cursor:
#         await cursor.execute("SELECT * from posts WHERE id = %s", (id))
#         new_post = await cursor.fetchone()        
#         if not new_post:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
#     return {"post_detail": new_post}


        
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id: int):
#     conn = await get_db_connection()
#     async with conn.cursor(aiomysql.DictCursor) as cursor:
#         # First, fetch the post to ensure it exists
#             await cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
#             deleted_post = await cursor.fetchone()

#             # If the post doesn't exist, raise a 404 error
#             if deleted_post is None:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

#             # Now, delete the post
#             await cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
#             await conn.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}")
# async def update_post(id: int, post: Post):
#     conn = await get_db_connection()
#     try:
#         async with conn.cursor(aiomysql.DictCursor) as cursor:
#             # Execute the UPDATE query
#             await cursor.execute(
#                 "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s",
#                 (post.title, post.content, post.published, id)
#             )
#             await conn.commit()

#             # Check if any rows were affected (if the post doesn't exist)
#             if cursor.rowcount == 0:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

#             # Fetch the updated post
#             await cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
#             updated_post = await cursor.fetchone()

#             if updated_post is None:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

#     except Exception as e:
#         # Handle any errors
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

#     finally:
#         # Ensure the connection is closed
#         if conn:
#             conn.close()

#     return {"data": updated_post}

    





# # @app.get("/posts/latest")
# # def get_latest_post():
# #     post = my_posts[len(my_posts)-1]
#     # return {"detail": post}

# # @app.post("/createpost")
# # def create_posts(payload: dict = Body(...)):
# #     return {"data": "Success add your posts"} 

# #Note :
# # Prural for naming API's (convention standard)
# # urutan di perhatikan jika latest di bawah {id} akan di akses yang atasnya
# # fastapi dev main.py