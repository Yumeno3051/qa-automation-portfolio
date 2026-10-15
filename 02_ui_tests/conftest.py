# conftest.py

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")

    # Убираем логи Chrome из консоли
    options.add_argument("--log-level=3")                                # только FATAL
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # отключить DevTools-логи

    # options.add_argument("--headless")  # запуск без окна браузера

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()