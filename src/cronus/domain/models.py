from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserSchema(BaseModel):
    id: int
    name: str = Field(..., min_lenght=2)
    email: str
    active: bool = True


class User(BaseModel):
    """Usuario tal como lo necesita el pipeline. Plano y validado."""

    model_config = ConfigDict(frozen=True)

    id: int = Field(gt=0)
    name: str = Field(min_length=2)
    email: EmailStr
    city: str
    company_name: str
    