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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from spawn_user_agent.user_agent import SpawnUserAgent
from webdriver_manager.chrome import ChromeDriverManager

# делаем случайный User Agent
user_agent = SpawnUserAgent.generate_all()

# прописываем опции для запуска браузера
option = Options()
option = webdriver.ChromeOptions()
option.add_argument("--incognito")  # режим инкогнито
option.add_argument("--disable-infobars")  # отключение всплывающих окон
option.add_argument("--start-maximized")  # включение полноэкранного режима
# option.add_argument("--headless=new")  # запуск без окна браузера
option.add_argument(f"--user_agent={random.choice(user_agent)}")

start_app_time = timer()  # начало отсчёта со старта программы

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
    "\n[INFO] Введите номер телефона без +7, привязянный к VK ID: "
)
phone_number_location.send_keys(phone_number_input)
time.sleep(5)
phone_number_location.send_keys(Keys.ENTER)

time.sleep(10)  # ждём, пока не придёт пуш-код

code_location = browser.find_element(
    By.XPATH,
    "/html/body/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[2]/div/div/input",
)  # находим поле для ввода кода
code_input = input(
    "\n[INFO] Введите код из пуш-уведомления на телефоне/электронной почты или 4 последние цифры номера телефона от звонка с Юлы: "
)
code_location.send_keys(code_input)

# начинаем взаимодействовать с самим сайтом
time.sleep(5)
print("[INFO] Перехожу на главную страницу Юлы...\n")
browser.get("https://youla.ru/")

print("[INFO] Жду появления всплывающего окна...\n")
time.sleep(5)

print("[INFO] Закрываю всплывающее окно с подтвержденем профиля...\n")
actions = ActionChains(browser)
actions.send_keys(Keys.ESCAPE)
actions.perform()

time.sleep(10)

# определяем URL архива неактивных объявлений в профиле
print(f"[INFO] Перехожу в профиль...\n")
browser.get("https://youla.ru/user")
time.sleep(10)

print(f"[INFO] Перехожу в архив неактивных объявлений в профиле...\n")
browser.find_element(
    By.XPATH,
    "/html/body/div[2]/div[1]/div[4]/main/div/div/div/section[2]/div/div[2]/div/div/ul/li[2]",
).click()

time.sleep(10)

# try:
#     # нажимаем на кнопку "Показать ещё" до упора, если она вообще есть
#     print("[INFO] Ищу кнопку <<Показать ещё>> и пытаюсь нажать на неё...\n")
#     browser.find_element(By.CLASS_NAME, "sc-ikHGee").click()
#     time.sleep(10)
# except:
#     print("[INFO] Кнопки <<Показать ещё>> нет на данной странице...")

# потом проходимся по всем неактивным объявлениям
print("[INFO] Собираю информацию о неактивных объявлениях...\n")
all_ads = browser.find_element(
    By.XPATH,
    "/html/body/div[2]/div[1]/div[4]/main/div/div/div/section[2]/div/div[2]/div/section",
).find_elements(By.CLASS_NAME, "sc-bvfSZU")

for i, ad in enumerate(all_ads):
    ad_name = ad.find_element(By.CLASS_NAME, "sc-fhlCRY").text
    ad_price = ad.find_element(By.CLASS_NAME, "sc-cOxWqc").text
    ad_image = ad.find_element(By.TAG_NAME, "image").get_attribute("xlink:href")
    print(i)
    print(
        f"""
        Название объявления: {ad_name}
        Цена в объявлении: {ad_price} рублей
        Изображения объявления: {ad_image}\n
        """
    )
    # browser.find_element(By.CLASS_NAME, "sc-islFiG").click()
    time.sleep(10)

overall_app_time = timer() - start_app_time  # общий подсчёт времени

# print(
#     """[INFO] Все неактивные объявления успешно продлены.
#       Работа программы завершена!\n"""
# )
print(f"[INFO] Общее время парсинга: {round(overall_app_time)} секунд(а).\n")
print("[INFO] Закрываю программу...")

browser.quit()
