from fastapi import HTTPException

class APIErrorCode:
    UNAUTHORIZED = HTTPException(status_code=401, detail="Unauthorized")
    INVALID_QUESTION_DATA = HTTPException(status_code=400, detail="Invalid question data")
    QUESTION_SET_NOT_EXIST = HTTPException(status_code=404, detail="Question set does not exist")
    QUESTION_NOT_FOUND = HTTPException(status_code=404, detail="Question not found")
    QUESTION_SET_NOT_FOUND = HTTPException(status_code=404, detail="Question set not found")
    LLM_SERVICE_ERROR = HTTPException(status_code=500, detail="LLM service error")
    UNAUTHORIZED_ACTION = HTTPException(status_code=403, detail="Unauthorized action")