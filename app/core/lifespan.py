from contextlib import asynccontextmanager

from app.core.logger import logger
from app.database.session import SessionLocal
from app.engine.client import engine
from app.services.platform.plans import PlanService


@asynccontextmanager
async def lifespan(app):

    db = SessionLocal()

    try:
        PlanService(db).seed_defaults()

        logger.info(
            "Default plans initialized."
        )

    finally:
        db.close()

    # -----------------------------------------------------
    # Engine Startup Check
    # -----------------------------------------------------

    try:

        health = await engine.health()

        version = await engine.version()

        logger.info(
            "Nativeee Engine connected (%s).",
            health["status"],
        )

        logger.info(
            "Engine Version: %s",
            version["version"],
        )

        logger.info(
            "Speech Provider: %s",
            version["providers"]["speech"],
        )

        logger.info(
            "Translation Provider: %s",
            version["providers"]["translation"],
        )

        logger.info(
            "Voice Provider: %s",
            version["providers"]["voice"],
        )

    except Exception as exc:

        logger.warning(
            "Nativeee Engine unavailable: %s",
            exc,
        )

    yield

    # -----------------------------------------------------
    # Shutdown Cleanup
    # -----------------------------------------------------

    await engine.close()