from models import Question, QuestionSet, get_session
from sqlmodel import Session, select

from dotenv import load_dotenv
import os

def create_question(db: Session, question: Question) -> str:
    # db.add(question)
    # db.commit()
    # db.refresh(question)
    print(question)
    return "success"

def create_question_set(db: Session, question_set: QuestionSet) -> str:
    # db.add(question_set)
    # db.commit()
    # db.refresh(question_set)
    print(question_set)
    return "success"