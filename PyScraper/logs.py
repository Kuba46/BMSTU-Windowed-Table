import logging
import os


# Получение пути к рабочему столу
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")


TARGET_URL = 'https://eu.bmstu.ru/modules/contingent3/'
LOGIN_URL = f'https://proxy.bmstu.ru:8443/cas/login?service={TARGET_URL}'
OUTPUT_FILE_NAME = os.path.join(desktop_path, 'eu_students.csv')
LOG_FILE_NAME = os.path.join(desktop_path, 'eu_students.log')
CREDENTIALS_FILE_NAME = 'credentials.json'


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # To stdout.
        logging.FileHandler(LOG_FILE_NAME, encoding="utf-8")  # To file.
    ]
)


logger = logging.getLogger()

