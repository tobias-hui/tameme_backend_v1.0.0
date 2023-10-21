from pydantic import BaseModel


class TxtRequest(BaseModel):
  input: str
