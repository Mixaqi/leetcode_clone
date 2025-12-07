from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserMixin(BaseModel):
    username: str = Field(min_length=3, max_length=40)
    email: EmailStr = Field(min_length=5)
    hashed_password: str = Field(min_length=8, max_length=100)

    @field_validator("hashed_password")
    @classmethod
    def password_strength(cls, hashed_password: str) -> str:
        if len(hashed_password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", hashed_password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", hashed_password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", hashed_password):
            raise ValueError("Password must contain at least one digit")
        return hashed_password


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
