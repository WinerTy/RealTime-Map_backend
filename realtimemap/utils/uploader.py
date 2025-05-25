import os
import shutil
import uuid
from pathlib import Path

from fastapi import File
from fastapi import HTTPException

from core.config import conf


def check_dir(sub_dir_name: str) -> Path:
    """
    Checks if a subdirectory exists within the main static directory and creates it if not.
    Returns the ABSOLUTE path to this subdirectory.
    :param sub_dir_name: Name of the subdirectory (e.g., "mark_photos", "user_avatars")
    :return: Absolute Path to the subdirectory
    """
    absolute_dir_path = conf.static / sub_dir_name
    os.makedirs(absolute_dir_path, exist_ok=True)
    return absolute_dir_path


async def upload_file(file: File(...), upload_sub_dir: str) -> str:
    """
    Saves the file to a subdirectory within the main static directory
    and returns a path RELATIVE to the main static directory.

    This relative path is suitable for storing in a database and later
    being used with `request.url_for(conf.STATIC_ROUTE_NAME, path=relative_path)`.

    :param file: File to upload (FastAPI File object)
    :param upload_sub_dir: Subdirectory within conf.STATIC_FILES_ROOT_DIR (e.g., "mark_photos")
                           This will be part of the returned relative path.
    :return: str: Relative path of the uploaded file (e.g., "mark_photos/unique_name.jpg")
    """
    absolute_target_dir = check_dir(upload_sub_dir)

    try:
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        absolute_file_save_path = absolute_target_dir / unique_filename

        with open(absolute_file_save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        relative_path_for_db = str(Path(upload_sub_dir) / unique_filename)

        return relative_path_for_db
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"File {file.filename} could not be uploaded. Error: {str(e)}",
        )
    finally:
        if file and hasattr(file, "close") and callable(file.close):
            await file.close()
