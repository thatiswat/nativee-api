import time

from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)


async def translate_text(
    text: str,
    source_language: str,
    target_language: str,
):
    start = time.perf_counter()

    prompt = f"""
Translate the following text.

Rules:
- Translate ONLY.
- Do not explain.
- Do not add quotation marks.
- Preserve names.
- Preserve punctuation.
- Output only the translated sentence.

Source Language: {source_language}
Target Language: {target_language}

Text:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    translated = (
        response.choices[0]
        .message.content
        .strip()
    )

    print(
        f"🌍 Groq Translation: {time.perf_counter()-start:.3f}s"
    )

    return translated