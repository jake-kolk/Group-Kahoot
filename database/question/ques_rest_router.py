from fastapi import APIRouter, Depends
from typing import Annotated

from models import Question, QuestionUpdate, get_session
from sqlmodel import Session, select

router = APIRouter()

@router.post("/questions/", response_model=Question)
def create_question(question: Annotated[Question, Depends()], db: Session = Depends(get_session)):
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

@router.put("/questions/{question_id}", response_model=Question)
def update_question(question_id: int, question: Annotated[QuestionUpdate, Depends()], db: Session = Depends(get_session)):
    updated_question = question.model_copy(update={"id": question_id})
    db.add(updated_question)
    db.commit()
    db.refresh(updated_question)
    return updated_question

@router.get("/questions/{question_id}", response_model=Question)
def read_question(question_id: int, db: Session = Depends(get_session)):
    question = db.exec(select(Question).where(Question.id == question_id)).first()
    return question

@router.get("/questions/", response_model=list[Question])
def read_questions(db: Session = Depends(get_session)):
    questions = db.exec(select(Question)).all()
    return questions