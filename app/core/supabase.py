import time

import httpx
import jwt

from app.core.settings import (
    SUPABASE_URL,
)


class SupabaseJWTVerifier:

    def __init__(self):
        self.jwks = None
        self.last_refresh = 0

    async def refresh_keys(self):
        """
        Download Supabase JWKS.
        Cache for one hour.
        """

        if (
            self.jwks is not None
            and time.time() - self.last_refresh < 3600
        ):
            return

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"
            )

            response.raise_for_status()

            self.jwks = response.json()

            self.last_refresh = time.time()

    async def verify(
        self,
        token: str,
    ):

        await self.refresh_keys()

        header = jwt.get_unverified_header(
            token,
        )

        kid = header.get(
            "kid",
        )

        key = next(
            (
                k
                for k in self.jwks["keys"]
                if k["kid"] == kid
            ),
            None,
        )

        if key is None:
            raise ValueError(
                "Unknown signing key."
            )

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(
            key,
        )

        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience="authenticated",
        )

        return payload


supabase = SupabaseJWTVerifier()