from deep_translator import GoogleTranslator
import time


async def translate_text(
    text: str,
    source_language: str,
    target_language: str,
):
    start = time.perf_counter()

    translated = GoogleTranslator(
        source="auto",
        target=target_language,
    ).translate(text)

    print(
        f"🌍 Google Translation: {time.perf_counter() - start:.3f}s"
    )

    return translated