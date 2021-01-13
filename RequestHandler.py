import config
import requests

from CommonUtils import create_df_from_json, create_df_to_ml_from_json, calculate_date_to_unix

API_KEY = config.keys['weathermap_api_key'] #on github there is empty key - you
# need to provide your own api key (for statistical data I had developer  plan (its paid))


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
    # actually it is not used but this project will be develop
    # so this method will stay (ignore DRY acronym)
    base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    result = requests.get(base_url.format(city, API_KEY))
    if result:
        result_json = result.json()
        coord_lon = result_json['coord']['lon']
        coord_lat = result_json['coord']['lat']
        base_url_one_call = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}'
        result_one_call = requests.get(base_url_one_call.format(coord_lat, coord_lon, '', API_KEY))
        result_one_call = result_one_call.json()
        mean_temp = (result_one_call['daily'][0]['temp']['day'] + result_one_call['daily'][0]['temp']['night'] +
                result_one_call['daily'][0]['temp']['eve'] + result_one_call['daily'][0]['temp']['morn']) / 4 #kelwin
        min_temp = result_one_call['daily'][0]['temp']['min']
        max_temp = result_one_call['daily'][0]['temp']['max']
        mean_humidity = result_one_call['daily'][0]['humidity']
        mean_pressure = result_one_call['daily'][0]['pressure']


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
        result_one_call = result_one_call.json()
        temp = result_one_call['daily'][date_diff]['temp']['day'] - 273.15 # temperature is described as kelvins
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
        base_url_one_call = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}'
        result_one_call = requests.get(base_url_one_call.format(coord_lat, coord_lon, 'minutely,alerts', API_KEY))
        result_one_call = result_one_call.json()
        dataframe = create_df_from_json(result_one_call)
        return dataframe


def get_data_for_ml_forecast(city):
    #it is not used as I did not have time and proper data to
    # implement neural network with tensorflow
    # openweathermap api documentation about history api is fatal and I have
    # no idea about parameters
    base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    result = requests.get(base_url.format(city, API_KEY))
    if result:
        result_json = result.json()
        coord_lon = result_json['coord']['lon']
        coord_lat = result_json['coord']['lat']
    ############################################3
    historical_data_url = 'http://history.openweathermap.org/data/2.5/history/city?' \
                          'lat={}&lon={}&type=hour&start={}&cnt={}&appid={}'

    # it will be used during development this project
    start_date = calculate_date_to_unix(1000)
    end_date_unix = calculate_date_to_unix(1)

    # ignore
    result_historical_data_call = requests.get(historical_data_url.format(coord_lon, coord_lat,'1580515200','', API_KEY))
    result_historical_data_call = result_historical_data_call.json()
    if result_historical_data_call['cod'] == '200':
        create_df_to_ml_from_json(result_historical_data_call['list'])


def get_statistical_data(city):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    result = requests.get(base_url.format(city, API_KEY))
    if result:
        result_json = result.json()
        coord_lon = result_json['coord']['lon']
        coord_lat = result_json['coord']['lat']

    statistical_data_url = 'https://history.openweathermap.org/data/2.5/aggregated/year?lat={}&lon={}&appid={}'
    data = requests.get(statistical_data_url.format(coord_lat, coord_lon, API_KEY)).json()['result']

    return data


def get_current_air_pollution_data(city):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    result = requests.get(base_url.format(city, API_KEY))
    if result:
        result_json = result.json()
        coord_lon = result_json['coord']['lon']
        coord_lat = result_json['coord']['lat']
        air_pollution_data_url = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}'
        data = requests.get(air_pollution_data_url.format(coord_lat, coord_lon, API_KEY)).json()
        co = data['list'][0]['components']['co']
        no = data['list'][0]['components']['no']
        o3 = data['list'][0]['components']['o3']
        so2 = data['list'][0]['components']['so2']
        pm2_5 = data['list'][0]['components']['pm2_5']
        pm10 = data['list'][0]['components']['pm10']
        nh3 = data['list'][0]['components']['nh3']

        return co, no, o3, so2, pm2_5, pm10, nh3


get_current_air_pollution_data('Kielce')
# not finished yet
# handle_df_for_dnn_regressor(df2)