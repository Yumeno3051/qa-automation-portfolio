# pages/login_page.py
"""Page Object для логина the-internet.herokuapp.com."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    URL = "https://the-internet.herokuapp.com/login"

    # Локаторы
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_MESSAGE = (By.ID, "flash")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a.button.secondary")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        return self

    def enter_username(self, username: str):
        field = self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
        field.clear()
        field.send_keys(username)
        return self

    def enter_password(self, password: str):
        field = self.driver.find_element(*self.PASSWORD_INPUT)
        field.clear()
        field.send_keys(password)
        return self

    def submit_login(self):
        """Кликает Login и ждёт перехода на /secure."""
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        # Ждём смены URL
        self.wait.until(lambda d: "/secure" in d.current_url or "login" in d.current_url)
        return self

    def get_flash_message(self) -> str:
        """Возвращает текст flash-сообщения."""
        message = self.wait.until(
            EC.visibility_of_element_located(self.FLASH_MESSAGE)
        )
        return message.text.strip()

    def is_logout_visible(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.LOGOUT_BUTTON))
            return True
        except Exception:
            return False