import os.path

import httpx
from fastapi.testclient import TestClient
from app.main import app
import logging

from sql_app import schemas

client = TestClient(app)

LOGGER = logging.getLogger(__name__)

files_dict = {
    "mp3_1mb": "https://file-examples.com/wp-content/storage/2017/11/file_example_MP3_1MG.mp3",
    "mp3_5mb": "https://file-examples.com/wp-content/storage/2017/11/file_example_MP3_5MG.mp3",
    "wav_5mp": "https://file-examples.com/wp-content/storage/2017/11/file_example_WAV_5MG.wav",
    "wav_10mp": "https://file-examples.com/wp-content/storage/2017/11/file_example_WAV_10MG.wav",
}


def test_read_main():
    response = client.get("/")
    assert response.history[0].status_code == 307
    assert response.status_code == 200


def download_song(file):
    if os.path.exists((file_path := files_dict[file].split("/")[-1])):
        return file_path
    url = files_dict[file]
    r = httpx.get(url, timeout=20)
    cdn_url = r.text[(r.text.find("file-examples.com/storage/")) :].split(";")[
        0
    ][:-2]
    url2 = files_dict[file].replace(
        "file-examples.com/wp-content/storage/", cdn_url
    )
    r = httpx.get(url2, timeout=20)
    with open(file_path, "wb") as f:
        f.write(r.content)
    return file_path


def test_wrong_filetype():
    response = client.post(
        "/inference",
        files={
            "file": (
                "a-long-way-166385.mp3",
                open(download_song("wav_5mp"), "rb"),
                "image/jpeg",
            )
        },
    )
    assert response.status_code == 415


def test_entity_too_large():
    response = client.post(
        "/inference",
        files={
            "file": (
                "a-long-way-166385.mp3",
                open(download_song("wav_10mp"), "rb"),
                "audio/mpeg",
            )
        },
    )
    assert response.status_code == 413


def test_response():
    response = client.post(
        "/inference",
        files={
            "file": (
                "a-long-way-166385.mp3",
                open(download_song("mp3_1mb"), "rb"),
                "audio/mpeg",
            )
        },
    )
    assert response.status_code == 200
    assert schemas.SongResponse.model_validate(response.json())


def test_cashed_song():
    for i in ["mp3_5mb", "mp3_5mb"]:
        response = client.post(
            "/inference",
            files={
                "file": (
                    i,
                    open(download_song(i), "rb"),
                    "audio/mpeg",
                )
            },
        )
        assert response.status_code == 200
        assert schemas.SongResponse.model_validate(response.json())
