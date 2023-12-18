from datetime import datetime

from pydantic import BaseModel


class Genre(BaseModel):
    """
    Parameters:
        id: int
        genre: string
    """

    id: int
    genre: str

    class ConfigDict:
        from_attributes = True


class ModelVersion(BaseModel):
    """
    Parameters:
        ml_model_hash: str
        ml_model_version: str
    """

    ml_model_hash: str
    ml_model_version: str

    class ConfigDict:
        from_attributes = True


class SongInference(BaseModel):
    """
    Parameters:
        song_hash:String
        genre_id: genre.id
        confidence:FLOAT
    """

    song_hash: str
    genre_id: str
    confidence: float

    class ConfigDict:
        from_attributes = True


class PostSongInference(SongInference):
    """
    Parameters:
        submitted:DATETIME
        ml_model_version: model_versions.ml_model_version
    """

    submitted: datetime
    ml_model_version: str


class SongResponse(BaseModel):
    """
    Parameters:
        genre:str
        confidence: float
    """

    genre: str
    confidence: float

    class ConfigDict:
        from_attributes = True
