import requests

from config.settings.development import APPID_OPENWEATHERMAP

url = 'https://api.openweathermap.org/data/2.5/weather'


def get_temperature(city: str = None) -> list:
    try:
        if city is None:
            return "City not defined"
        params = {
            'q': city,
            'long': 'ru',
            'appid': APPID_OPENWEATHERMAP,
            'units': 'metric'
        }
        response = requests.get(
            url=url,
            params=params
        )
        res = response.json()
        # print()
        info_dict = {
            'temperature': res['main']['temp'],
            'country': res['sys']['country'],
            'icon': res['city'][0]['icon']
        }
        return info_dict
    except KeyError:
        return 'error'
