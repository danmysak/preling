from .gemini import read as gemini_read
from .openai import read as openai_read

__all__ = [
    'read',
]

GEMINI_PREFIX = 'gemini'


def read(text: str, language: str, model: str, api_key: str) -> None:
    """Read the given text using either OpenAI's or Gemini's TTS service."""
    (
        gemini_read
        if model.lower().startswith(GEMINI_PREFIX)
        else openai_read
    )(text, language, model, api_key)
