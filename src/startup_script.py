import argparse
from pathlib import Path

from sql_app import database
from sql_app.database import engine, get_db_conxt
from sql_app.models import Genre, ModelVersions


def main():
    parser = argparse.ArgumentParser(
        description="Auto Generate Configs and files for your evaluation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--data_path",
        help="Path for general file storage",
        default="data",
        type=Path,
    )
    parser.add_argument(
        "-c",
        "--conf_file",
        help="Path to conf file",
        default="data",
        type=Path,
    )
    args = parser.parse_args()
    config = vars(args)

    genres = [
        {"id": 1, "name": "Metal"},
        {"id": 2, "name": "Rock"},
        {"id": 3, "name": "Pop"},
        {"id": 4, "name": "Jazz"},
    ]

    model_versions = [
        {"model_hash": "blabla", "version": "0.0.1"},
        {"model_hash": "blabla2", "version": "0.0.2"},
    ]
    # Create folder
    Path(config["data_path"]).mkdir(parents=True, exist_ok=True)
    print(f'Created Data folder as {config["data_path"]}')

    # Generate Models
    for i in model_versions:
        with open(
            (config["data_path"] / f"model{i['version']}.bin"), "wb"
        ) as f:
            f.seek(1 * 1024 * 1024 * 1024 - 1)
            f.write(b"\0")
    print("Generated Fake models")

    database.Base.metadata.create_all(bind=engine)

    # Populate Genres Table
    with get_db_conxt() as db:
        for i in genres:
            db.add(
                Genre(id=i["id"], genre=i["name"]),
            )
        try:
            db.commit()
        except Exception as e:
            print(e)
    print("Generated Genres")

    # Populate ModelVersions Table
    with get_db_conxt() as db:
        for i in model_versions:
            db.add(
                ModelVersions(
                    ml_model_hash=i["model_hash"],
                    ml_model_version=i["version"],
                )
            )
        try:
            db.commit()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
