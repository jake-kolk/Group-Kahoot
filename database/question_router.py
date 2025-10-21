from fastapi import APIRouter, Depends
from sqlmodel import Session
from database.models import get_session
from database.question_api import get_questions, get_question, create_question
from database.models import Question

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("/")
def read_questions(db: Session = Depends(get_session)):
    return get_questions(db)

@router.get("/{question_id}")
def read_question(question_id: int, db: Session = Depends(get_session)):
    return get_question(question_id, db)

@router.post("/")
def add_question(question: Question, db: Session = Depends(get_session)):
    return create_question(question, db)
