from fastapi import UploadFile
import httpx

from app.core.settings import ENGINE_URL


class EngineClient:

    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(120),
            limits=httpx.Limits(
                max_keepalive_connections=20,
                max_connections=100,
            ),
        )

    async def conversation(
        self,
        audio: UploadFile,
        source_language: str,
        target_language: str,
    ):
        audio.file.seek(0)

        files = {
            "audio": (
                audio.filename,
                audio.file,
                audio.content_type
                or "audio/mpeg",
            ),
        }

        data = {
            "source_language": source_language,
            "target_language": target_language,
        }

        response = await self.client.post(
            f"{ENGINE_URL}/conversation",
            files=files,
            data=data,
        )

        response.raise_for_status()

        return response.json()

    async def conversation_stream(
        self,
        audio: UploadFile,
        source_language: str,
        target_language: str,
    ):
        audio.file.seek(0)

        files = {
            "audio": (
                audio.filename,
                audio.file,
                audio.content_type
                or "audio/mpeg",
            )
        }

        data = {
            "source_language": source_language,
            "target_language": target_language,
        }

        request = self.client.build_request(
            "POST",
            f"{ENGINE_URL}/conversation/stream",
            files=files,
            data=data,
        )

        response = await self.client.send(
            request,
            stream=True,
        )

        response.raise_for_status()

        return response

    async def health(
        self,
    ):
        response = await self.client.get(
            f"{ENGINE_URL}/health",
        )

        response.raise_for_status()

        return response.json()

    async def version(
        self,
    ):
        response = await self.client.get(
            f"{ENGINE_URL}/version",
        )

        response.raise_for_status()

        return response.json()

    async def close(
        self,
    ):
        await self.client.aclose()


engine = EngineClient()