from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver


class DriverSetup:
    def setup(self) -> WebDriver:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        return webdriver.Chrome(options=chrome_options)
