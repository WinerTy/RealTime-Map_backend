import logging

from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from geojson_pydantic import Point

logger = logging.getLogger(__name__)


def serialization_geom(geom: WKBElement) -> Point:
    try:
        result = to_shape(geom)
        return Point(**result.__geo_interface__)
    except Exception as e:
        logger.error(e)
        return None
