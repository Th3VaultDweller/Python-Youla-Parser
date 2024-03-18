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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from webdriver_manager.chrome import ChromeDriverManager

# прописываем опции для запуска браузера
option = Options()
option = webdriver.ChromeOptions()
# option.add_argument("--incognito")  # режим инкогнито
option.add_argument("--disable-infobars")  # отключение всплывающих окон
option.add_argument("--start-maximized")  # включение полноэкранного режима
option.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# берём драйвер для работы Selenium
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser = webdriver.Chrome(options=option)

# определяем URL архива неактивных объявлений в профиле
# каждый URL - уникален для каждого пользователя сайта
url = "https://youla.ru/user/5a81fe12f235023e6447afc4/archive"
browser.get(url)
print(f"[INFO] Перехожу по адресу {url}...\n")

time.sleep(120)

try:
    browser.find_element(By.CLASS_NAME, "sc-ikHGee eamdVs").click()
    time.sleep(10)

except:
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
