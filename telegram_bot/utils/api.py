import requests
import os
from django.core.signing import Signer

signer = Signer(key=os.getenv("DJANGO_SECRET_KEY"), fallback_keys=[])


class API:
    backend_url = os.getenv('BACKEND_API_URL')

    def __init__(self, tg_id: int) -> None:
        self.tg_id = tg_id
        self.headers = {
            'Authentication': signer.sign(str(tg_id))
        }

    def _get(self, relative_url: str) -> tuple[dict | list, int]:
        response = requests.get(
            self.backend_url + relative_url,
            headers=self.headers
        )
        return (response.json(), response.status_code)

    def _post(self, relative_url: str, **kwargs) -> tuple[dict, int]:
        response = requests.post(
            self.backend_url + relative_url,
            data=kwargs, headers=self.headers
        )
        return (response.json(), response.status_code)

    def get_profile(self) -> tuple[dict, int]:
        return self._get('profile/')

    def create_user(self, first_name: str, location: str | None = None,
                    lat: float | None = None, lon: float | None = None,
                    last_name: str | None = None, age: int | None = None,
                    bio: str | None = None, **kwargs) -> tuple[dict, int]:

        return self._post(
            'profile/create/',
            tg_id=self.tg_id, first_name=first_name, last_name=last_name,
            age=age, location=location, lat=lat, lon=lon, bio=bio
        )

    def get_trips(self) -> tuple[list, int]:
        return self._get('trips/')

    def get_trip(self, trip_id: int) -> tuple[dict, int]:
        return self._get(f'trips/{trip_id}/')

    def create_trip(self, name: str,
                    description: str | None = None) -> tuple[dict, int]:
        return self._post('trips/', name=name, description=description)

    def add_location(self, trip_id: int, start_date: str, end_date: str,
                     query: str | None = None, lat: float | None = None,
                     lon: float | None = None) -> tuple[dict, int]:
        return self._post(
            f'trips/{trip_id}/add_location/',
            query=query, lat=lat, lon=lon,
            start_date=start_date, end_date=end_date
        )
