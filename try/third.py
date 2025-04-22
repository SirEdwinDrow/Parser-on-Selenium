from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.chrome.service import Service as ChromeService


# Инициализация веб-драйвера
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # Режим без графического интерфейса
driver_path = "paste the folder path/try/chromedriver-win64/chromedriver.exe"
#driver = webdriver.Chrome(executable_path=driver_path)
service = ChromeService(executable_path=driver_path)  # <= передаем путь в Service
driver = webdriver.Chrome(service=service)
# URL сайта с прогнозом погоды
url = "https://yandex.ee/pogoda/ru/moscow/details?lang=ru&via=ms"


try:
   # Переход на сайт
   driver.get(url)
   time.sleep(3)  # Ожидание загрузки страницы


   # Сбор данных о погоде
   days = driver.find_elements(By.XPATH, '//p[@class="sc-77074498-0 eCkVRF"]')
   temperatures = driver.find_elements(By.XPATH, '//div[@style="grid-area: temperature-morning; padding: 10px 0px;"]')
   precipitations = driver.find_elements(By.CLASS_NAME, 'sc-ea88bf5a-2.isUibM')
   pressures = driver.find_elements(By.XPATH, '//div[@style="grid-area: pressure-day;"]')
   humidities = driver.find_elements(By.XPATH, '//div[@style="grid-area: humidity-day;"]')
   wind_speeds = driver.find_elements(By.XPATH, '//div[@style="grid-area: wind-day;"]')


   # Формирование списка с данными
   weather_data = []
   for i in range(len(days)):
       day = days[i].text.split("\n") if i < len(days) else ["N/A", "N/A"]
       date = day[0]  # Например: "6 апреля"
       description = day[1] if len(day) > 1 else "N/A"  # Например: "сегодня"
       temp = temperatures[i].text if i < len(temperatures) else "N/A"
       precip = precipitations[i].text if i < len(precipitations) else "N/A"
       pressure = pressures[i].text if i < len(pressures) else "N/A"
       humidity = humidities[i].text if i < len(humidities) else "N/A"
       wind = wind_speeds[i].text if i < len(wind_speeds) else "N/A"
       weather_data.append([date, description, temp, precip, pressure, humidity, wind])


   # Создание DataFrame
   columns = ["Дата", "Описание дня", "Температура", "Осадки", "Давление", "Влажность", "Скорость ветра"]
   df = pd.DataFrame(weather_data, columns=columns)


   # Сохранение в CSV
   df.to_csv("weather_forecast.csv", index=False, encoding='utf-8-sig')
   print("Данные сохранены в файл weather_forecast.csv")


finally:
   # Закрытие драйвера
   driver.quit()
