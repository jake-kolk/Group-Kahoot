from fastapi import APIRouter, Depends
from typing import Annotated

from auth.auth_handler import get_current_active_user

from models import Question, QuestionUpdate, get_session, User, QuestionSet
from sqlmodel import Session, select
from database.api_error_code import APIErrorCode

router = APIRouter()

# CRUD operations for Question
@router.post("/questions/", response_model=Question)
def create_question(question: Question, 
                    db: Session = Depends(get_session),
                    current_user: User = Depends(get_current_active_user)):
    db_question = Question.model_validate(question)
    if not db_question:
        raise APIErrorCode.INVALID_QUESTION_DATA
    
    question_set = db.get(QuestionSet, question.question_set)
    if not question_set:
        raise APIErrorCode.QUESTION_SET_NOT_EXIST

    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.put("/questions/{question_id}", response_model=Question)
def update_question(question_id: int,
                    question: QuestionUpdate, 
                    db: Session = Depends(get_session), 
                    current_user: User = Depends(get_current_active_user)):
    db_question = db.get(Question, question_id)
    if not db_question:
        raise APIErrorCode.QUESTION_NOT_FOUND

    for key, value in question.model_dump(exclude_unset=True).items():
        setattr(db_question, key, value)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.get("/questions/{question_id}", response_model=Question)
def read_question(question_id: int, 
                  db: Session = Depends(get_session),
                  current_user: User = Depends(get_current_active_user)):
    question = db.exec(select(Question).where(Question.id == question_id)).first()
    if not question:
        raise APIErrorCode.QUESTION_NOT_FOUND
    return question

@router.get("/questions/{question_set_id}", response_model=list[Question])
def read_questions(question_set_id: int, 
                   db: Session = Depends(get_session),
                   current_user: User = Depends(get_current_active_user)):
    questions = db.exec(select(Question).where(Question.question_set == question_set_id)).all()
    if not questions:
        raise APIErrorCode.QUESTION_NOT_FOUND
    return questions

@router.delete("/questions/{question_id}", response_model=Question)
def delete_question(question_id: int, 
                    db: Session = Depends(get_session),
                    current_user: User = Depends(get_current_active_user)):
    question = db.get(Question, question_id)
    if not question:
        raise APIErrorCode.QUESTION_NOT_FOUND
    db.delete(question)
    db.commit()
    return question


# CRUD operations for QuestionSet

@router.post("/question_sets/", response_model=QuestionSet)
def create_question_set(question_set: QuestionSet, 
                        db: Session = Depends(get_session),
                        current_user: User = Depends(get_current_active_user)):
    db.add(question_set)
    db.commit()
    db.refresh(question_set)
    return question_set

@router.get("/question_sets/{user_id}", response_model=list[QuestionSet])
def read_question_sets(user_id: int, 
                       db: Session = Depends(get_session),
                       current_user: User = Depends(get_current_active_user)):
    question_sets = db.exec(select(QuestionSet).where(QuestionSet.user_id == user_id)).all()
    if not question_sets:
        raise APIErrorCode.QUESTION_SET_NOT_FOUND
    return question_sets

@router.delete("/question_sets/{question_set_id}", response_model=QuestionSet)
def delete_question_set(question_set_id: int, 
                        db: Session = Depends(get_session),
                        current_user: User = Depends(get_current_active_user)):
    question_set = db.get(QuestionSet, question_set_id)
    if not question_set:
        raise APIErrorCode.QUESTION_SET_NOT_FOUND
    db.delete(question_set)
    db.commit()
    return question_set

@router.put("/question_sets/{question_set_id}", response_model=QuestionSet)
def update_question_set(question_set_id: int,
                        question_set: QuestionSet, 
                        db: Session = Depends(get_session), 
                        current_user: User = Depends(get_current_active_user)):
    db_question_set = db.get(QuestionSet, question_set_id)
    if not db_question_set:
        raise APIErrorCode.QUESTION_SET_NOT_FOUND

    for key, value in question_set.model_dump(exclude_unset=True).items():
        setattr(db_question_set, key, value)
    db.add(db_question_set)
    db.commit()
    db.refresh(db_question_set)
    return db_question_set
