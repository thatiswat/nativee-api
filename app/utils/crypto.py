import hashlib
import secrets


def generate_api_key(live: bool = True) -> str:
    """
    Generate a secure Nativeee API key.
    """

    prefix = "ntv_live_" if live else "ntv_test_"

    return prefix + secrets.token_urlsafe(32)


def hash_api_key(api_key: str) -> str:
    """
    Hash an API key before storing it.
    """

    return hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()