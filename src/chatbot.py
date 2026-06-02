from src.config import get_openai_client
from src.prompts import ANSWER_STYLE_INSTRUCTIONS, SYSTEM_PROMPT


def ask_chatbot(question: str, knowledge_base: str, answer_style: str) -> str:
    try:
        client = get_openai_client()

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": f"""
Knowledge base:
{knowledge_base}

Answer style:
{answer_style}

Question:
{question}

{ANSWER_STYLE_INSTRUCTIONS}
""",
                },
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    except Exception as error:
        return (
            "Sorry, something went wrong while generating the answer. "
            "This may be related to API quota, connectivity, or configuration.\n\n"
            f"Technical error: `{error}`"
        )
