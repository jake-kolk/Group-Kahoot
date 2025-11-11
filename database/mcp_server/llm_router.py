from fastapi import APIRouter, Depends

from auth.auth_handler import get_current_active_user

from models import User
from sqlmodel import Session, select
from api_error_code import APIErrorCode

from llm_service import tinyLlama_service

router = APIRouter()

@router.post("/generate_quiz")
async def generate_quiz(topic:str,
                        description: str = None,
                        num_questions: int = 5,
                        current_user: User = Depends(get_current_active_user)):
    result = await tinyLlama_service.generate_quiz_content(topic, num_questions)
    if "error" in result:
        raise APIErrorCode.LLM_SERVICE_ERROR
    return result
