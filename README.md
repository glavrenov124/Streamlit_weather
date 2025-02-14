# Streamlit_weather

## 📜 Описание
Данный проект представляет собой веб-приложение, реализованное с помощью **Streamlit**, которое позволяет:
- Анализировать **текущую температуру** в различных городах мира.
- Сравнивать её с **историческими данными** для этих городов.

## 🗂️ Структура проекта
Проект организован в виде папки `streamlit_app`, содержащей следующие файлы:

### 1. **`app.py`**
   - Основной файл веб-приложения.
   - Реализует логику интерфейса и взаимодействия с пользователем.
   - Подключает функции из других файлов для обработки данных.

### 2. **`requirements.txt`**
   - Содержит список необходимых библиотек для запуска приложения.

### 3. **`analysis_function.py`**
   - Включает функции, используемые в `app.py`:
     - Анализ исторических данных.
     - Получение текущей температуры (например, через API).
   - Содержит синхронные и асинхронные методы для работы с данными.

### 4. **`Analiz_DZ.ipynb`**
   - Jupyter Notebook, демонстрирующий процесс выполнения домашнего задания:
     - Загрузка и анализ исторических данных.
     - Получение текущей температуры.
     - Использование различных синхронных и асинхронных методов
    -  Файл не используется в самом приложении
    
