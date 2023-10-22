from pydantic import BaseModel
from typing import Optional


class visualglm(BaseModel):
  text: Optional[str] = "请描述这张图片的内容"
  image_url: str
  history: Optional[list] = []
