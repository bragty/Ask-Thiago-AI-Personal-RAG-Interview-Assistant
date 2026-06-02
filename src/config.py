import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


def get_openai_api_key() -> str:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY was not found. "
            "Set it in your local .env file or in Streamlit Cloud secrets."
        )

    return api_key


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=get_openai_api_key())
