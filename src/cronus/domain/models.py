from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    id: int
    name: str = Field(..., min_lenght=2)
    email: str
    active: bool = True
