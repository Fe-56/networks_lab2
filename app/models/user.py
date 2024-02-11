from pydantic import BaseModel

class User(BaseModel):
  userID: str = None
  name: str = None
  password: str = None