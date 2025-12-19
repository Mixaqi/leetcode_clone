import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, ConfigDict

class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        return v

class CreateUser(UserLogin):
    username: str = Field(min_length=3, max_length=40)
    confirm_password: str = Field(min_length=8, max_length=100)

    @model_validator(mode="after")
    def check_passwords_match(self) -> CreateUser:
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

class SessionData(BaseModel):
    user_id: int
    created_at: datetime