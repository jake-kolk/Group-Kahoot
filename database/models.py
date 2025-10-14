from sqlmodel import Field, create_engine, SQLModel, Session, Column, JSON, Relationship
from typing import Optional, List
from dotenv import load_dotenv
import os

class UserBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    admin: bool = False

class User(UserBase, table=True):
    hashed_password: str = Field()

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    admin: Optional[bool] = None


class QuestionSet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    user_id: int = Field(foreign_key="user.id")

class QuestionBase(SQLModel):
    question_set: int = Relationship(back_populates="questions")
    question_text: str
    choices: List[str] = Field(sa_column=Column(JSON))
    correct_answer: str

class Question(QuestionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class QuestionUpdate(QuestionBase):
    question_text: Optional[str] = None
    choices: Optional[List[str]] = Field(sa_column=Column(JSON), default=None)
    correct_answer: Optional[str] = None


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, echo=True)
SQLModel.metadata.create_all(engine)

# Dependency
def get_session():
    with Session(engine) as session:
        yield session