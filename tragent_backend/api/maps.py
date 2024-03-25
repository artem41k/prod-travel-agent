from django.conf import settings
from rest_framework.exceptions import APIException
from OSMPythonTools.nominatim import Nominatim, NominatimResult
from routingpy import ORS, exceptions
from PIL.Image import Image
from staticmap import StaticMap, Line, CircleMarker
import os

from . import models


class OSM:
    query_params = {
        'addressdetails': 1,
        'accept-language': 'ru'
    }
    query_zoom = 10  # 'zoom = 10' means city level in OSM API

    def __init__(self) -> None:
        self.nominatim = Nominatim()

    def _get_data_from_result(
            self, result: NominatimResult) -> tuple[str, str, dict]:
        for data in result.toJSON():
            country = data['address'].get('country')
            if addr_city := data['address'].get('city'):
                return addr_city, country, data
            elif addr_city := data['address'].get('province'):
                return addr_city, country, data
        return ('', '', {})

    def get_city_by_name(self, name: str) -> tuple[str, str, dict]:
        return self._get_data_from_result(
            self.nominatim.query(name, params=self.query_params)
        )

    def get_city_by_coords(
            self, lat: float, lon: float) -> tuple[str, str, dict]:
        return self._get_data_from_result(
            self.nominatim.query(
                lat, lon, reverse=True, zoom=self.query_zoom,
                params=self.query_params
            )
        )


def render_map(route: list[list], points: list[dict]) -> Image:
    smap = StaticMap(
        settings.ROUTE['MAP']['WIDTH'],
        settings.ROUTE['MAP']['HEIGHT'],
    )
    for coords in route:
        smap.add_line(
            Line(
                [coords],
                settings.ROUTE['LINE']['COLORS']['MAIN'],
                settings.ROUTE['LINE']['WIDTH']
            )
        )
    for point in points:
        smap.add_marker(
            CircleMarker(
                point['coords'],
                point['color'],
                point['width']
            )
        )
    return smap.render()


def generate_route(
        locations: models.Location,
        home: models.Location | None = None) -> tuple[Image, int]:
    ors = ORS(api_key=os.getenv('ORS_API_KEY'))
    try:
        route = ors.directions(
            [
                [loc.lon, loc.lat] for loc in locations
            ],
            profile='driving-car'
        )
    except exceptions.RouterApiError as exc:
        # 2004 is ORS api error code, that means
        # "The approximated route distance must not be greater
        # than 6000000.0 meters" (or 6000 km)
        if '2004' in exc.message:
            detail = '2004'
        else:
            detail = ''
        raise APIException(detail, code=400)

    points = []
    for loc in locations:
        color = settings.ROUTE['POINT']['COLORS']['MAIN']
        if home:
            if loc.lon == home.lon and loc.lat == home.lat:
                color = settings.ROUTE['POINT']['COLORS']['HOME']
        points.append({
            'coords': [loc.lon, loc.lat],
            'color': color,
            'width': settings.ROUTE['POINT']['WIDTH']
        })

    map_img = render_map(route.geometry, points)

    return map_img, route.distance
