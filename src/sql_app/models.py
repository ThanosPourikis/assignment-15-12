from sqlalchemy import Column, String, DATETIME, FLOAT, INT, ForeignKey
from sqlalchemy.orm import mapped_column

from sql_app.database import Base


class SongInference(Base):
    """
    Parameters:
        song_hash:String
        genre_id: genre.id
        confidence:FLOAT
        submitted:DATETIME
        model_version: model_versions.ml_model_version
    """

    __tablename__ = "song_inferences"

    song_hash = Column(String, primary_key=True, index=True)
    genre_id = Column(INT, ForeignKey("genre.id"))
    confidence = Column(FLOAT)
    submitted = Column(DATETIME)
    model_version = mapped_column(
        ForeignKey("model_versions.ml_model_version")
    )


class Genre(Base):
    """
    Parameters:
        id: int
        genre: string
    """

    __tablename__ = "genre"

    id = Column(INT, primary_key=True, index=True)
    genre = Column(String, unique=True)


class ModelVersions(Base):
    """
    Parameters:
        ml_model_hash: str
        ml_model_version: str
    """

    __tablename__ = "model_versions"

    ml_model_hash = Column(String, primary_key=True, index=True)
    ml_model_version = Column(String, unique=True)
