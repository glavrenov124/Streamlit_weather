import pandas as pd 
import requests
import datetime
from sklearn.linear_model import LinearRegression
def analysis_temperature_of_city(df, city):
    # Фильтр по городу
    df_city = df.loc[df['city'] == city].copy()

    #Основные показатели
    avg_temp = df_city['temperature'].mean()
    min_temp = df_city['temperature'].min()
    max_temp = df_city['temperature'].max()


    # Скользящее среднее и стандартное отклонение за 30 дней
    df_city['roll_mean_30_days'] = df_city['temperature'].rolling(window=30).mean()
    df_city['roll_std_30_days'] = df_city['temperature'].rolling(window=30).std()

    # Поиск аномалий
    df_city['anomaly'] = (
        (df_city["temperature"] < 
         (df_city["roll_mean_30_days"] - 2 * df_city["roll_std_30_days"])) |
        (df_city["temperature"] > 
         (df_city["roll_mean_30_days"] + 2 * df_city["roll_std_30_days"]))
    )
    
    anomalies = df_city.loc[df_city['anomaly']]
    # Профиль по сезонам
    profile_of_season = df_city.groupby('season', as_index=False).agg(
        temperature_mean=('temperature', 'mean'),
        temperature_std=('temperature', 'std')
    )
    
    
    df_city['timestamp'] = pd.to_datetime(df_city['timestamp'])
    df_city['days'] = (df_city['timestamp'] - df_city['timestamp'].min()).dt.days
    X = df_city[['days']]
    y = df_city['temperature']
    model = LinearRegression()
    model.fit(X, y)
    trend_slope = model.coef_[0]



    return {
        "city": city,
        "df_city": df_city,
        "avg_temp": avg_temp,
        "min_temp": min_temp,
        "max_temp": max_temp,
        "anomalies": anomalies,
        "profile_of_season": profile_of_season,
        "trend_slope": trend_slope

    }

def get_current_temp_of_city(API_KEY, city):
    URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(URL)
    current_datetime = datetime.datetime.now()
    month_of_temp = current_datetime.month

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        return temperature, month_of_temp
    else:
        raise Exception(f" Ошибка при получении данных с сайта OpenWeather: {response.status_code}, {response.text}")
    
def temperature_is_normal_or_not(city, profile_of_season, temperature, month_of_temp):
    current_season = month_to_season_mapping.get(month_of_temp)
    profile_of_season = profile_of_season.query('season == @current_season')

    
    mean_temp = profile_of_season['temperature_mean'].iloc[0]
    std_temp = profile_of_season['temperature_std'].iloc[0]

    lower_bound = mean_temp - 2 * std_temp
    upper_bound = mean_temp + 2 * std_temp 

    if lower_bound <= temperature <= upper_bound:
        return f"The temperature {temperature}°C in {city} is NORMAL for {current_season}."
    else:
        return f"The temperature {temperature}°C in {city} is NOT NORMAL for {current_season}."
    

month_to_season_mapping = {
    1: "winter",
    2: "winter",
    3: "spring",
    4: "spring",
    5: "spring",
    6: "summer",
    7: "summer",
    8: "summer",
    9: "autumn",
    10: "autumn",
    11: "autumn",
    12: "winter",
     }