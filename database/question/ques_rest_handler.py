from models import Question, get_session
from sqlmodel import Session, select

from dotenv import load_dotenv
import os

def create_question(db: Session, question: Question) -> Question:
    db.add(question)
    db.commit()
    db.refresh(question)
    return question