from OSMPythonTools.nominatim import Nominatim, NominatimResult


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
            if data['addresstype'] == 'city':
                city = data['address']['city']
                country = data['address']['country']
                return city, country, data
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
