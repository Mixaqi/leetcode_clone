from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserMixin(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(min_length=5)

class CreateUser(UserMixin):
    pass

class UserSchema(UserMixin):
    id: int
    hashed_password: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class SessionData(BaseModel):
    user_id: int
    created_at: datetime