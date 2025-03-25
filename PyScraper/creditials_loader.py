from logs import logger
import json
import os



class CredentialsLoader:
    def __init__(self, filename: str):
        self.filename = filename

    def load(self):
        logger.info(f'Loading credentials from file: {self.filename}.')

        if not os.path.exists(self.filename):
            raise FileNotFoundError(
                f'File with credentials not found: {self.filename}.'
            )

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                credentials = json.load(file)
                if 'login' not in credentials or 'password' not in credentials:
                    raise ValueError(
                        f'Invalid credentials file: {self.filename}.'
                    )
                logger.info('Credentials loaded successfully.')
                return credentials['login'], credentials['password']
        except json.JSONDecodeError:
            raise ValueError(
                f'Invalid JSON format in file: {self.filename}.'
            )