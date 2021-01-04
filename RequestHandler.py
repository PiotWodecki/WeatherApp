import requests, json
from configparser import ConfigParser

from CommonUtils import create_df_from_json

API_KEY = 'aa0baa3fb2e5da05f1c1c2beee420b4e'

# config_file = 'config.ini'
# config = ConfigParser()
# config.read(config_file)
# api_key = config['api_key']['key']


base_url2 = 'http://api.openweathermap.org/data/2.5/weather?'

# city_name = input("City: ")

def get_weather(city):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    result = requests.get(base_url.format(city, API_KEY))
    if result:
        result_json = result.json()
        city_name = result_json['name']
        country_name = result_json['sys']['country']
        temp_kelvin = result_json['main']['temp']
        pressure = result_json['main']['pressure']
        humidity = result_json['main']['humidity']
        wind_speed = result_json['wind']['speed']
        temp_celsius = temp_kelvin - 273.15
        icon = result_json['weather'][0]['icon']
        weather = result_json['weather'][0]['main']
        weather_description = result_json['weather'][0]['description']
        final = (city_name, country_name, temp_celsius, icon, weather, weather_description, pressure, humidity, wind_speed)

        return final
    else:
        return None


def get_forecast(city):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    result = requests.get(base_url.format(city, API_KEY))
    if result:
        result_json = result.json()
        coord_lon = result_json['coord']['lon']
        coord_lat = result_json['coord']['lat']
        print(coord_lat, coord_lon)
        base_url_one_call = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}'
        result_one_call = requests.get(base_url_one_call.format(coord_lat, coord_lon, '', API_KEY))
        print(result_one_call.json())
        result_one_call = result_one_call.json()
        mean_temp = (result_one_call['daily'][0]['temp']['day'] + result_one_call['daily'][0]['temp']['night'] +
                result_one_call['daily'][0] ['temp']['eve'] + result_one_call['daily'][0]['temp']['morn']) / 4 #kelwin
        min_temp = result_one_call['daily'][0]['temp']['min']
        max_temp = result_one_call['daily'][0]['temp']['max']
        mean_humidity = result_one_call['daily'][0]['humidity']
        mean_pressure = result_one_call['daily'][0]['pressure']
        print(mean_temp, min_temp, max_temp, mean_humidity, mean_pressure)


def get_regular_forecast(city, date_diff):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    result = requests.get(base_url.format(city, API_KEY))
    if result:
        result_json = result.json()
        coord_lon = result_json['coord']['lon']
        coord_lat = result_json['coord']['lat']
        city_name = result_json['name']
        country_name = result_json['sys']['country']
        base_url_one_call = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}'
        result_one_call = requests.get(base_url_one_call.format(coord_lat, coord_lon, 'minutely,hourly', API_KEY))
        # print(result_one_call.json())
        result_one_call = result_one_call.json()
        temp = result_one_call['daily'][date_diff]['temp']['day'] - 273.15
        pressure = result_one_call['daily'][date_diff]['pressure']
        humidity = result_one_call['daily'][date_diff]['humidity']
        wind_speed = result_one_call['daily'][date_diff]['wind_speed']
        weather = result_one_call['daily'][date_diff]['weather'][0]['main']
        weather_desc = result_one_call['daily'][date_diff]['weather'][0]['description']
        weather_icon = result_one_call['daily'][date_diff]['weather'][0]['icon']
        final = (city_name, country_name, temp, weather_icon, weather, weather_desc, pressure, humidity, wind_speed)
        return final


def get_forecast_for_plot(city):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    result = requests.get(base_url.format(city, API_KEY))
    if result:
        result_json = result.json()
        coord_lon = result_json['coord']['lon']
        coord_lat = result_json['coord']['lat']
        city_name = result_json['name']
        country_name = result_json['sys']['country']
        base_url_one_call = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}'
        result_one_call = requests.get(base_url_one_call.format(coord_lat, coord_lon, 'minutely,alerts', API_KEY))
        result_one_call = result_one_call.json()
        dataframe = create_df_from_json(result_one_call)
        return dataframe
