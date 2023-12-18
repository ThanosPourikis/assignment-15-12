import asyncio
import os
from datetime import datetime
from logging import Logger
from typing import Dict

from sqlalchemy.orm import Session

from sql_app import models as models, schemas


async def post_inference(
    db: Session, response: Dict, song_hash: str, model_version: str
):
    if os.environ.get("DISABLE_DB", False):
        return 0
    result = (
        db.query(models.SongInference.song_hash)
        .filter(
            models.SongInference.song_hash == song_hash,
            models.SongInference.model_version == model_version,
        )
        .first()
    )
    if not result:
        song_inference = models.SongInference(
            song_hash=song_hash,
            genre_id=response["genre"],
            confidence=response["confidence"],
            submitted=datetime.now(),
            model_version=model_version,
        )
        db.add(song_inference)
        db.commit()


async def search_song(
    db: Session,
    song_hash: str,
    genres: Dict[int, str],
    request_id: str,
    logger: Logger,
) -> schemas.SongResponse | None:
    """Search db for previous inference
    Parameters:
            db: Database Session
            song_hash: hash of song
            genres: Genre Mapper
            request_id: Request Id
            logger: Project logger
    """
    if os.environ.get("DISABLE_DB", False):
        return None
    # Simulate Db latency
    logger.info(f"Searching Db for {request_id} result")
    await asyncio.sleep(0.10)
    result = (
        db.query(
            models.SongInference.genre_id, models.SongInference.confidence
        )
        .filter(models.SongInference.song_hash == song_hash)
        .first()
    )
    if result:
        return schemas.SongResponse.model_validate(
            {"genre": genres[result[0]], "confidence": result[1]}
        )
    else:
        return None
