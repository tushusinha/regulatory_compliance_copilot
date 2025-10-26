"""
LLM Client Module
Handles interaction with OpenAI or compatible LLM endpoints.
"""

from langchain_openai import ChatOpenAI
from loguru import logger
from dotenv import load_dotenv


class LLMClient:
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.api_key = api_key

        if not self.api_key:
            logger.warning("⚠️ No OPENAI_API_KEY found. Running in mock mode.")
        else:
            logger.info("✅ OpenAI API key loaded successfully.")

        logger.info(f"Initializing LLM client with model: {model_name}")
        self.client = ChatOpenAI(
            model=model_name,
            temperature=0.2,
            api_key=api_key
        )

    def generate_text(self, prompt: str) -> str:
        """Generate a text completion using the LLM."""
        try:
            response = self.client.invoke(prompt)
            return response.content
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return "Error: LLM request failed."

    def summarize_text(self, text: str, max_length: int = 300) -> str:
        """Summarize long regulatory text for compliance overview."""
        prompt = f"Summarize this document for compliance officers (max {max_length} words):\n\n{text}"
        return self.generate_text(prompt)
