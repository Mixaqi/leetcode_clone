import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserMixin(BaseModel):
    username: str = Field(min_length=3, max_length=40)
    email: EmailStr = Field(min_length=5)
    password: str = Field(min_length=8, max_length=100)

    @field_validator("password")
    @classmethod
    def password_strength(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", password):
            raise ValueError("Password must contain at least one digit")
        return password


class CreateUser(UserMixin):
    pass


class UserSchema(UserMixin):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SessionData(BaseModel):
    user_id: int
    created_at: datetime
