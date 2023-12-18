# Ml model size simulation #
import asyncio
import os
from logging import Logger
from random import uniform, choice
from typing import Dict

from fastapi import UploadFile


class MlModel:
    def __init__(self, version: str):
        self.version = version
        with open(
            f'{os.environ.get("DATA_FOLDER", "data")}/model{version}.bin', "rb"
        ) as f:
            self.model = f.read()

    async def predict(
        self, music_file: UploadFile, request_id: str, logger: Logger
    ) -> Dict[str:int, str:float]:
        """
        Simulate Model prediction

        Parameters:
            request_id: Request Id
            logger: Project logger

        Return:
            Prediction
        """
        # Simulate Compute
        logger.info(f"Computing {request_id} result")
        await asyncio.sleep(uniform(0.5, 2))
        return {"genre": choice(range(1, 4)), "confidence": uniform(0.5, 1)}
