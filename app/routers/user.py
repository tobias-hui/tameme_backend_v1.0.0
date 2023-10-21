from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from app.models.user import User, UserLogin, UserRegister
from app.core.db import database, users_table
import sqlite3
from fastapi.responses import JSONResponse

router = APIRouter(tags=["User"])


@router.post("/register/")
async def register(user: UserRegister):
  query = users_table.insert().values(
      nickname=user.nickname,
      city="BeiJing",  # 默认值
      coins=0  # 默认值
  )
  try:
    last_record_id = await database.execute(query)
    return {
        "id": last_record_id,
        "nickname": user.nickname,
        "avatar_url": None,
        "city": "BeiJing",  # 默认值
        "coins": 0  # 默认值
    }
  except sqlite3.IntegrityError:
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content={"detail": "Nickname is already taken"})


@router.post("/login/")
async def login(user: UserLogin):
  query = users_table.select().where(users_table.c.nickname == user.nickname)
  user_in_db = await database.fetch_one(query)
  if user_in_db:
    return {
        "id": user_in_db["id"],
        "nickname": user_in_db["nickname"],
        "avatar_url": user_in_db["avatar_url"],
        "city": user_in_db["city"],
        "coins": user_in_db["coins"]
    }
  raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )


@router.get("/users/{user_id}/", response_model=User)
async def get_user(user_id: int):
  query = users_table.select().where(users_table.c.id == user_id)
  user_in_db = await database.fetch_one(query)
  if user_in_db:
    return user_in_db
  raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/{user_id}/", response_model=User)
async def update_user(user_id: int, user: User):
  query = (users_table.update().where(users_table.c.id == user_id).values(
      nickname=user.nickname,
      avatar_url=user.avatar_url,
      city=user.city,
      coins=user.coins))
  await database.execute(query)

  # 获取更新后的用户信息
  query = users_table.select().where(users_table.c.id == user_id)
  updated_user = await database.fetch_one(query)

  if updated_user:
    return updated_user
  raise HTTPException(status_code=404, detail="User not found")
