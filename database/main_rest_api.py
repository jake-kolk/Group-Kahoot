import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import auth.auth_router as auth_router
import auth.user_router as user_router
import question.ques_rest_router as ques_router

app = FastAPI(debug=True)

origin = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/auth")
app.include_router(user_router.router)
app.include_router(ques_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


