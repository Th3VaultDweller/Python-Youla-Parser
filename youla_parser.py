import csv
import datetime
import json
import random
import time
from timeit import default_timer as timer

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from webdriver_manager.chrome import ChromeDriverManager

# прописываем опции для запуска браузера
option = Options()
option = webdriver.ChromeOptions()
option.add_argument("--incognito")  # режим инкогнито
option.add_argument("--disable-infobars")  # отключение всплывающих окон
option.add_argument("--start-maximized")  # включение полноэкранного режима
option.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# берём драйвер для работы Selenium
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser = webdriver.Chrome(options=option)

# логинимся на сайт
print(f"[INFO] Перехожу на страницу логина Юлы...\n")

browser.get("https://youla.ru/login")
time.sleep(5)

phone_number_location = browser.find_element(
    By.XPATH,
    "/html/body/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/section/div/div/div/input",
)  # находим поле для ввода номера телефона
phone_number_input = input(
    "[INFO] Введите  номер телефона без +7, привязянный к VK ID: "
)
phone_number_location.send_keys(phone_number_input)
time.sleep(5)
phone_number_location.send_keys(Keys.ENTER)

time.sleep(30)  # ждём, пока не придёт пуш-код
code_location = browser.find_element(
    By.XPATH,
    "/html/body/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[2]/div/div/input",
)
code_input = input(
    "[INFO] Введите код из пуш-уведомления на телефоне/электронной почты или 4 последние цифры номера телефона, от звонка с Юлы: "
)
code_location.send_keys(code_input)

time.sleep(120)

try:
    # закрываем всплывающее окно с подтверждением профиля
    browser.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/div[22]/div/div/div/main/div/div/div/div[1]/i"
    ).click()
except:
    pass

time.sleep(10)

# определяем URL архива неактивных объявлений в профиле
# каждый URL - уникален для каждого пользователя сайта
# сделать browser.find_element и взять url профиля с главной страницы юлы + передать это браузеру для перехода в архив
url = browser.find_element(
    By.CLASS_NAME, "sc-gGvHcT sc-iqPaeV klBUgP chFKKW"
).get_attribute("href")
browser.get(url)
print(f"[INFO] Перехожу по адресу {url+'/archive'}...\n")

time.sleep(10)

try:
    # нажимаем на кнопку "Показать ещё" до упора, если она вообще есть
    browser.find_element(By.CLASS_NAME, "sc-ikHGee eamdVs").click()
    time.sleep(10)

except:
    # потом проходимся по всем неактивным объявлениям
    all_ads = browser.find_element(By.CLASS_NAME, "sc-jOiSOi gpQJHO").find_elements(
        By.CLASS_NAME, "sc-bvfSZU ffvCCB"
    )

    for ad in all_ads:
        ad_name = ad.find_element(
            By.CLASS_NAME, "sc-cOxWqc sc-fhlCRY bOrVyP khXenE"
        ).text
        ad_price = ad.find_element(By.CLASS_NAME, "sc-fxhZON fzJDlO").text
        ad_image = ad.find_element(By.TAG_NAME, "image").get_attribute("href")

        print(
            f"""
            Название объявления: {ad_name}\n
            Цена в объявлении: {ad_price}\n
            Изображения объявления: {ad_image}\n
            """
        )
        time.sleep(10)

print("[INFO] Работа программы завершена!")

browser.quit()
