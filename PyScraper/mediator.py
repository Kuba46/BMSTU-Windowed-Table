from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logs import logger, CREDENTIALS_FILE_NAME, TARGET_URL
import json
import os


class Mediator(object):
    def load_credentials(filename: str):
        logger.info(f'Loading credentials from file: {filename}.')

        if not os.path.exists(filename):
            raise FileNotFoundError(
                f'File with credentials not found: {filename}.'
            )

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                credentials = json.load(file)
                if 'login' not in credentials or 'password' not in credentials:
                    raise ValueError(
                        f'Invalid credentials file: {filename}.'
                    )
                logger.info('Credentials loaded successfully.')
                return credentials['login'], credentials['password']
        except json.JSONDecodeError:
            raise ValueError(
                f'Invalid JSON format in file: {filename}.'
            )

    def auth(driver: WebDriver, url: str):
        logger.info(f'Authenticating on the website: {url}.')
        login, password = Mediator.load_credentials(CREDENTIALS_FILE_NAME)
        driver.get(url)

        # The website requires double authentication on the first
        # attempt after browser restart.
        # This is a known behavior: the form resets after the first submission.
        for i in range(2):
            logger.info(f'Trying to authenticate {i + 1}.')
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username')))
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'password')))

            username_field.send_keys(login)
            password_field.send_keys(password)

            # Save URL to wait for redirection.
            current_url = driver.current_url

            login_button = driver.find_element(By.NAME, 'submit')
            login_button.click()

            try:
                # Wait until the URL changes.
                WebDriverWait(driver, 10).until(
                    EC.url_changes(current_url)
                )
            except Exception:
                raise ValueError('Failed to authenticate.')

        WebDriverWait(driver, 10).until(EC.url_contains(TARGET_URL))
        logger.info('Successfully authenticated.')

    