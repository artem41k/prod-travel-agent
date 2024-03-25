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
        return response.json(), response.status_code

    def _post(self, relative_url: str, **kwargs) -> tuple[dict, int]:
        response = requests.post(
            self.backend_url + relative_url,
            data=kwargs, headers=self.headers
        )
        return response.json(), response.status_code

    def _patch(self, relative_url: str, data: dict) -> tuple[dict, int]:
        response = requests.patch(
            self.backend_url + relative_url,
            data=data, headers=self.headers
        )
        return response.json(), response.status_code

    def _delete(self, relative_url: str) -> int:
        response = requests.delete(
            self.backend_url + relative_url,
            headers=self.headers
        )
        return response.status_code

    def _get_content(self, relative_url: str) -> tuple[bytes, int]:
        response = requests.get(
            self.backend_url + relative_url,
            headers=self.headers
        )
        status_code = response.status_code
        content = response.content if status_code == 200 else response.json()
        return content, response.headers, status_code

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

    def update_user(self, **kwargs) -> tuple[dict, int]:
        return self._patch(
            'profile/',
            data=kwargs
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

    def delete_location(self, trip_id: int,
                        location_id: int) -> tuple[dict, int]:
        return self._post(
            f'trips/{trip_id}/delete_location/',
            location_id=location_id
        )

    def get_route(self, trip_id: int) -> tuple[bytes, int]:
        return self._get_content(f'trips/{trip_id}/route/')

    def update_trip(self, trip_id: int, **kwargs) -> tuple[dict, int]:
        return self._patch(f'trips/{trip_id}/', data=kwargs)

    def delete_trip(self, trip_id: int) -> int:
        return self._delete(f'trips/{trip_id}/')
