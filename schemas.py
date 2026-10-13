from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------- Users ----------
class UserCreate(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    full_name: str | None = None
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = Field(default=None, min_length=8)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: EmailStr
    full_name: str | None
    disabled: bool
    role: str


# ---------- Auth ----------
class Token(BaseModel):
    access_token: str
    token_type: str


# ---------- Notes ----------
class NoteCreate(BaseModel):
    title: str
    content: str
    is_public: bool = False
    tags: list[str] = []


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    is_public: bool | None = None
    tags: list[str] | None = None


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    owner: str
    is_public: bool
    created_at: datetime
    tags: list[str]