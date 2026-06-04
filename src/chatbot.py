from src.config import get_openai_client
from src.prompts import ANSWER_STYLE_INSTRUCTIONS, SYSTEM_PROMPT


def ask_chatbot(question: str, retrieved_context: str, answer_style: str) -> str:
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
Retrieved context:
{retrieved_context}

Answer style:
{answer_style}

Question:
{question}

Use only the retrieved context above to answer.
If the answer is not available in the retrieved context, say that the information is not available in the knowledge base.
Do not invent details.
Keep the answer useful for recruiters and interviewers.
Mention the source files used at the end when possible.

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
