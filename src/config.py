import os

from dotenv import load_dotenv
from openai import OpenAI


def get_openai_client() -> OpenAI:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Add it to your local .env file before running the app."
        )

    return OpenAI(api_key=api_key)
