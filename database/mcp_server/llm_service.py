# !pip install llama-cpp-python

from huggingface_hub import hf_hub_download
import os
import httpx
import json
import logging
import typing

logger = logging.getLogger("tinyllama-mcp")

repo_id = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
filename = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
if not os.path.exists(filename):
    model_path = hf_hub_download(repo_id=repo_id, filename=filename, local_dir='.')


class TinyLlamaService:
    def __init__(self, mcp_server_url: str = 'http://localhost:8001'):
        self.mcp_server_url = mcp_server_url
        
    async def generate_questions(self, topic: str, count: int = 5, difficulty: str ='medium') -> dict:
        """
        Generating quiz questions using tinyllama
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.mcp_server_url}/generate_quiz",
                    json={
                        "topic": topic,
                        "num_questions": count,
                        "difficulty": difficulty
                    },
                    timeout=60.0
                )
                return response.json()
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return {"error": str(e)}
        
    
    async def generate_quiz_content(self, topic: str, num_questions: int) -> dict:
        """
        Generate complete quiz content
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.mcp_server_url}/generate_quiz_content",
                    json={
                        "topic": topic,
                        "num_questions": num_questions
                    },
                    timeout=60.0
                )
                return response.json()
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return {"error": str(e)}

tinyLlama_service = TinyLlamaService()
