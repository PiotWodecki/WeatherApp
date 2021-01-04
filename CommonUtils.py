import pandas as pd

from datetime import datetime, timedelta


def create_df_from_json(json):
    dates = []
    dates2 = []
    temps = []
    print(json)
    print()
    for x in json['daily']:
        dates.append(datetime.utcfromtimestamp(int(x['dt'])).strftime('%d/%m/%Y'))
    for x in dates:
        for y in range(4):
            dates2.append((datetime.strptime(x, '%d/%m/%Y') + timedelta(hours=y*6)))

    for index, date in enumerate(dates2):
        dates2[index] =datetime.strftime(date, '%d/%m/%Y %H:%M')
    print(dates2)

    for index, day in enumerate(json['daily']):
        temps.append(day['temp']['night'] - 273.15)
        temps.append(day['temp']['morn'] - 273.15)
        temps.append(day['temp']['day'] - 273.15)
        temps.append(day['temp']['eve'] - 273.15)
    print(temps)
    print(len(temps))
    print(len(dates2))

    df = pd.DataFrame(
        {'Dates': dates2,
        'Temperatures': temps})
    df['Dates'] = pd.to_datetime(df['Dates'], format='%d/%m/%Y %H:%M')

    return df

