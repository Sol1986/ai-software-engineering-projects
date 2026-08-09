"""
separate the LLM behavior from the FastAPI route. 
This is an important production pattern: the route handles HTTP, 
while a dedicated client handles AI-provider work.
"""

from typing import (
    Protocol,  # a Python tool for describing what methods a class must have.
)


# “Anything used as an LLMClient must have a generate method that accepts text and returns text.”
class LLMClient(Protocol):
    # self refers to the particular LLMService object using the method.
    def generate(self, business_request: str, context: dict[str, str]) -> str:
        """Generate an answer for a business request."""

class PlaceholderLLMClient:
    def generate(self, business_request: str, context: dict[str, str]) -> str:
        return f"Placeholder response for: {business_request}"

def get_llm_client() -> LLMClient: #1 (see main.py for usage)
    return PlaceholderLLMClient()