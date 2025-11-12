from fastmcp import FastMCP
import logging
import json
import os
from llama_cpp import Llama

from question.ques_rest_handler import *
from models import *

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tinyllama-mcp")

mcp = FastMCP(name="Quiz_Generator")

MODEL_PATH = "./tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "512"))

logger.info(f"Loading model from {MODEL_PATH} with temperature={TEMPERATURE} and max_tokens={MAX_TOKENS}")
llm = Llama(model_path=MODEL_PATH, temperature=TEMPERATURE, max_tokens=MAX_TOKENS)

# @mcp.prompt()
# def generate_quiz(topic: str, num_questions: int) -> str:
#     """
#     Generate a quiz based on the given topic and number of questions.
#     """
#     return f"Generating a quiz on '{topic}' with {num_questions} questions. The questions will have 4 multiple-choice answers each."

'''
@mcp.tool()
def generate_quiz_questions(topic: str, count: int, difficulty: str ='medium') -> str:
    """
    Generating quiz questions with 4 choicesusing tinyllama

    Args:
        topic: The topic of the quiz
        count: Number of questions to generate
        difficulty: Difficulty level of the questions

    Returns:
        a JSON containing the generated questions
    """

    count = max(1, min(count, 20))  # Ensure count is between 1 and 20

    prompt = (
        f"Generate {count} quiz questions on the topic '{topic}' with difficulty level '{difficulty}'. "
        "Each question should have 4 multiple-choice answers (A, B, C, D) and indicate the correct answer. "
        """For EACH question, use this EXACT JSON format:
        {{
        "question": "The question text here?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": "Option A",
        "explanation": "Why this answer is correct"
        }
        """
    )
    response = llm(prompt, temperature=TEMPERATURE)

    try:
        text = response['choices'][0]['text'].strip()
        # Attempt to parse the response as JSON
        start_index = text.find('[')
        end_index = text.rfind(']') + 1
        if start_index != -1 and end_index > start_index:
            json_str = text[start_index:end_index]
            questions = json.loads(json_str)
            return {
                "success": True,
                "topic": topic,
                "difficulty": difficulty,
                "count": len(questions),
                "questions": questions
            }
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")

    return {
        "success": False,
        "error": "Failed to parse generated questions.",
        "raw_response": text
    }
'''

@mcp.tool()
def create_new_question_set(question_set: QuestionSet) -> str:
    """
    Create a new question set in the database

    Args:
        question_set: The QuestionSet object containing title, description, and user_id

    Returns:
        A success or failure message
    """
    # Here you would add the logic to insert the question set into your database
    # For demonstration, we will just log the question set and return a success message

    create_question_set(get_session(), question_set)

    logger.info(f"Creating new question set in database: {question_set}")
    return "Question set created successfully in the database."

@mcp.tool()
def insert_question(quiz_json: Question)->str:
    """
    Insert generated quiz into the database

    Args:
        quiz_json: The JSON containing the quiz data

    Returns:
        A success or failure message
    """
    # Here you would add the logic to insert the quiz into your database
    # For demonstration, we will just log the quiz and return a success message

    for question in quiz_json.questions:
        create_question(get_session(), question)

    logger.info(f"Inserting quiz into database: {quiz_json}")
    return "Quiz inserted successfully into the database."


if __name__ == "__main__":
    mcp.run(transport="stdio")