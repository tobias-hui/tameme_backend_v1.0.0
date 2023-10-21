from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
  nickname: str  # 用户昵称
  avatar_url: Optional[str] = None  # 用户头像
  city: Optional[str] = "BeiJing"  # 用户所处城市
  coins: int = 0  # 用户的金币数量，默认为0

class UserRegister(BaseModel):
  nickname: str

class UserLogin(BaseModel):
  nickname: str