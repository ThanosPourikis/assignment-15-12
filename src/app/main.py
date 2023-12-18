import logging
from hashlib import md5
from uuid import uuid4

from fastapi import FastAPI, UploadFile, Request, Depends, responses
from fastapi.exceptions import HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session

from ml_model.ml_model import MlModel
from sql_app import schemas, models
from sql_app.database import get_db, get_db_conxt
from sql_app.interface import post_inference, search_song

logger = logging.getLogger(__name__)

app = FastAPI()
Instrumentator().instrument(app).expose(app)


def start_up():
    global model
    model = MlModel("0.0.1")

    global GENRES
    with get_db_conxt() as db:
        GENRES = {
            i[0]: i[1]
            for i in db.query(models.Genre.id, models.Genre.genre).all()
        }


start_up()


@app.get("/")
async def read_root():
    return responses.RedirectResponse(url="/docs")


@app.post("/inference")
async def inference(
    request: Request, file: UploadFile, db: Session = Depends(get_db)
) -> schemas.SongResponse:
    requsest_id = str(uuid4())
    logger.info(f"Request received {requsest_id}")
    if int(request.headers.get("content-length")) >= 10 * 1024 * 1024:
        # more than 10 MB
        # But should be handled at frontend
        logger.info(f"Request:{requsest_id} returned 413")
        raise HTTPException(status_code=413)
    if file.content_type != "audio/mpeg":
        # Check file format
        logger.info(f"Request:{requsest_id} returned 415")
        raise HTTPException(status_code=415)

    song_hash = md5(file.file.read()).hexdigest()

    # Search db for previous inference
    result = await search_song(db, song_hash, GENRES, requsest_id, logger)
    if result:
        logger.info(f"Request:{requsest_id} returned cashed result")
        return result

    response = await model.predict(file, requsest_id, logger)
    await post_inference(db, response, song_hash, model.version)
    logger.info(f"Request:{requsest_id} Uploaded to DB")
    response["genre"] = GENRES[response["genre"]]
    logger.info(f"Request:{requsest_id} returned cashed result")
    return response
