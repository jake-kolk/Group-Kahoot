from database.models import Question, QuestionUpdate, get_session
from sqlmodel import Session, select
from typing import List, Optional

def create_question(question: Question, db: Session = get_session()):
    db_question = Question.model_validate(question)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_question(question_id: int, db: Session = get_session()):
    question = db.get(Question, question_id)
    return question

def get_questions(db: Session = get_session()):
    questions = db.exec(select(Question)).all()
    return questions