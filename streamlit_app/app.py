import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
from analysis_function import analysis_temperature_of_city, get_current_temp_of_city, temperature_is_normal_or_not
from sklearn.linear_model import LinearRegression
st.title("Анализ и мониторинг погоды")

st.sidebar.header("Настройки")
uploaded_file = st.sidebar.file_uploader("Загрузите CSV файл с историческими данными", type=["csv"])
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
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, parse_dates=['timestamp'])
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    cities = data['city'].unique()
    city = st.sidebar.selectbox("Выберите город", cities)

    city_results = analysis_temperature_of_city(data, city)

    city = city_results['city']
    df_city = city_results['df_city']
    avg_temp = city_results['avg_temp']
    min_temp = city_results['min_temp']
    max_temp = city_results['max_temp']
    anomalies = city_results['anomalies']
    profile_of_season = city_results['profile_of_season']
    trend_slope = city_results['trend_slope']

    with st.expander(f"Описательная статистика для {city}"):
        st.write(f"Средняя температура: {avg_temp}°C")
        st.write(f"Минимальная температура: {min_temp}°C")
        st.write(f"Максимальная температура: {max_temp}°C")

    st.subheader("Временной ряд температур")
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(
    df_city['timestamp'], 
    df_city['temperature'], 
    label="Температура", 
    color='blue'
)

# Отметка аномалий (если они есть)
    if not anomalies.empty:  # Проверка на наличие данных в anomalies
        ax.scatter(
            anomalies['timestamp'], 
            anomalies['temperature'], 
            color='red', 
            label="Аномалии", 
            zorder=5
        )

# Линия средней температуры
    ax.axhline(
        y=avg_temp, 
        color='green', 
        linestyle='--', 
        label="Средняя температура"
    )

# Настройка заголовка и подписей осей
    ax.set_title("Временной ряд температур", fontsize=14)
    ax.set_xlabel("Дата", fontsize=12)
    ax.set_ylabel("Температура (°C)", fontsize=12)
    ax.legend()
    st.pyplot(fig)
    
    st.subheader("Сезонный профиль температуры")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(
        profile_of_season['season'], 
        profile_of_season['temperature_mean'], 
        yerr=profile_of_season['temperature_std'], 
        capsize=5, 
        color=['orange', 'green', 'red', 'blue'], 
        alpha=0.8
    )

    ax.set_title("Средняя температура по сезонам", fontsize=14)
    ax.set_ylabel("Температура (°C)", fontsize=12)
    ax.set_xlabel("Сезон", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    st.pyplot(fig)

    st.subheader("Оценка тренда температуры")
    if trend_slope > 0:
        st.write(f"Тренд положительный: температура увеличивается на {round(trend_slope, 5)}°C/день ")
    else:
        st.write(f"Тренд отрицательный: температура уменьшается на {round(trend_slope, 5)}°C/день ")

    st.subheader("Текущая погода")
    api_key = st.text_input("Введите API ключ OpenWeatherMap", type="password")
    if api_key:
        current_temp, current_month = get_current_temp_of_city(api_key, city)
        st.write(f"Текущая температура в городе {city}: {current_temp}°C")

        is_temp_normal = temperature_is_normal_or_not(city, profile_of_season, current_temp, current_month)
        st.write(is_temp_normal)
