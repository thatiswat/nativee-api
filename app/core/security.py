import hashlib
import secrets

PREFIX_LIVE = "ntv_live_"
PREFIX_TEST = "ntv_test_"


def generate_api_key(live: bool = True) -> str:
    """
    Generate a secure Nativeee API key.
    """

    prefix = PREFIX_LIVE if live else PREFIX_TEST

    token = secrets.token_urlsafe(32)

    return f"{prefix}{token}"


def hash_api_key(api_key: str) -> str:
    """
    Hash an API key before storing it.
    """

    return hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()


def verify_api_key(
    api_key: str,
    stored_hash: str,
) -> bool:

    return hash_api_key(api_key) == stored_hash