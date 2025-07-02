from typing import Any, Optional, Union, List

from pydantic import ValidationInfo
from starlette.requests import Request

from core.config import conf


def generate_full_image_url(
    value: Any,
    info: ValidationInfo,
) -> Optional[Union[str, List[str]]]:
    if not value:
        return None

    request: Optional[Request] = info.context.get("request") if info.context else None

    def _generate_url(photo_obj: Any) -> Optional[str]:
        if not photo_obj:
            return ""

        if request:
            print("Реализация через request")
            return str(
                request.url_for(
                    "get_file",
                    storage=photo_obj.upload_storage,
                    file_id=photo_obj.file_id,
                )
            )

        base_url = conf.server.base_url

        file_url = photo_obj.path
        print(f"{base_url}/media/{file_url}")
        return f"{base_url}/media/{file_url}"

    if isinstance(value, list):
        return [_generate_url(photo) for photo in value if photo]

    if isinstance(value, str):  # TODO SEE THIS MB BAGS
        return value

    return _generate_url(value)
