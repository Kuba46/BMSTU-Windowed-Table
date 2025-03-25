from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logs import logger, TARGET_URL


class AuthHandler:
    def __init__(self, url: str, credentials_loader):
        self.url = url
        self.credentials_loader = credentials_loader

    def authenticate(self, driver: WebDriver):
        logger.info(f'Authenticating on the website: {self.url}.')
        login, password = self.credentials_loader.load()
        driver.get(self.url)

        for i in range(2):
            logger.info(f'Trying to authenticate {i + 1}.')
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username')))
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'password')))

            username_field.send_keys(login)
            password_field.send_keys(password)

            current_url = driver.current_url
            login_button = driver.find_element(By.NAME, 'submit')
            login_button.click()

            try:
                WebDriverWait(driver, 10).until(EC.url_changes(current_url))
            except Exception:
                raise ValueError('Failed to authenticate.')

        WebDriverWait(driver, 10).until(EC.url_contains(TARGET_URL))
        logger.info('Successfully authenticated.')
