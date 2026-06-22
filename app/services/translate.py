from deep_translator import GoogleTranslator

async def translate_text(
    text: str,
    source_language: str,
    target_language: str
):
    translated = GoogleTranslator(
        source="auto",
        target=target_language
    ).translate(text)

    return translated