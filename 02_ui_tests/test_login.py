# test_login.py
"""
UI-тесты логина на the-internet.herokuapp.com.
Демонстрируют: Page Object, ожидания, позитивные и негативные сценарии.
"""

from pages.login_page import LoginPage


class TestLogin:
    """Тесты формы логина."""

    def test_successful_login(self, driver):
        """Позитивный тест: успешный вход с валидными данными."""
        page = LoginPage(driver).open()
        page.enter_username("tomsmith").enter_password("SuperSecretPassword!").submit_login()

        message = page.get_flash_message()
        assert "You logged into a secure area!" in message, \
            f"Ожидалось сообщение об успехе, получено: {message}"
        assert page.is_logout_visible(), "Кнопка Logout не появилась"

    def test_login_with_wrong_password(self, driver):
        """Негативный тест: неверный пароль."""
        page = LoginPage(driver).open()
        page.enter_username("tomsmith").enter_password("WrongPassword").submit_login()

        message = page.get_flash_message()
        assert "Your password is invalid!" in message, \
            f"Ожидалось сообщение об ошибке пароля, получено: {message}"

    def test_login_with_wrong_username(self, driver):
        """Негативный тест: неверный логин."""
        page = LoginPage(driver).open()
        page.enter_username("wrong_user").enter_password("SuperSecretPassword!").submit_login()

        message = page.get_flash_message()
        assert "Your username is invalid!" in message, \
            f"Ожидалось сообщение об ошибке логина, получено: {message}"

    def test_login_with_empty_fields(self, driver):
        """Негативный тест: пустые поля."""
        page = LoginPage(driver).open()
        page.submit_login()

        message = page.get_flash_message()
        assert "Your username is invalid!" in message, \
            f"Ожидалось сообщение об ошибке, получено: {message}"