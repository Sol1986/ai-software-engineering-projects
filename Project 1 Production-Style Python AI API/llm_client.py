"""
Making OpenAILLMClient a class is a good idea because it represents one configured OpenAI client that can be reused.
client = OpenAILLMClient(settings)

That object can remember its own:
API key
model name
OpenAI SDK connection
future settings such as timeout or retry limit

Then every request can simply call:
client.generate(business_request, context)
instead of passing the API key and model into a separate function every time.
"""

import json
from typing import Annotated, Protocol

from fastapi import Depends
from openai import OpenAI

from settings import Settings, get_settings


class LLMConfigurationError(Exception):
    """Raised when LLM configuration is incomplete or unsupported."""


class LLMProviderError(Exception):
    """Raised when the LLM provider cannot return an answer."""


# “Anything used as an LLMClient must have a generate method that accepts text and returns text.”
class LLMClient(Protocol):
    # self refers to the particular LLMService object using the method.
    def generate(self, business_request: str, context: dict[str, str]) -> str:
        """Generate an answer for a business request."""

class OpenAILLMClient: # Creates a blueprint for an OpenAI LLM client.

    #__init__ runs means “initialize.” automatically when you create the client:
    def __init__(self, settings: Settings) -> None:
        self._api_key = settings.llm_api_key
        self._model = settings.llm_model

    def generate(self, business_request: str, context: dict[str, str]) -> str:
        if not self._api_key:
            raise LLMConfigurationError("OpenAI API key is not configured.")

        client = OpenAI(api_key=self._api_key)

        try:
            response = client.responses.create(
                model=self._model,
                instructions=(
                    "You are a practical business assistant. "
                    "Give concise, actionable answers. "
                    "State important uncertainty when relevant."
                ),

                input=(
                    f"Business request:\n{business_request}\n\n"
                    f"Context (JSON):\n{json.dumps(context)}" # creates one text string containing your context dictionary in JSON format.
                ),
                store=False,
            )

        except Exception as error:
            raise LLMProviderError(
                "The LLM provider could not generate a response.") from error

        answer = response.output_text.strip()

        if not answer:
            raise LLMProviderError("The LLM provider returned no text.")

        return answer




def get_llm_client(settings: Annotated[Settings, Depends(get_settings)]) -> LLMClient: #1 (see main.py for usage)
    return OpenAILLMClient(settings)