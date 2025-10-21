from database.models import Question, QuestionUpdate, get_session
from sqlmodel import Session, select
from typing import List, Optional


def get_question(question_id: int, db: Session = get_session()):
    question = db.get(Question, question_id)
    return question

def get_questions(question_set_id: int, db: Session = get_session()):
    questions = db.exec(select(Question).where(Question.question_set == question_set_id)).all()
    return questions