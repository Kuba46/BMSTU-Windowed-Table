from auth_handler import AuthHandler
from creditials_loader import CredentialsLoader
from driver_setup import DriverSetup
from link_finder import LinkFinder
from mediator import Mediator
from parser import Parser
from writer import Writer

from logs import logger, CREDENTIALS_FILE_NAME, LOGIN_URL


def main():
    try:
        logger.info('Starting the script.')
        driver_setup = DriverSetup()
        credentials_loader = CredentialsLoader(CREDENTIALS_FILE_NAME)
        auth_handler = AuthHandler(LOGIN_URL, credentials_loader)
        parser = Parser()
        link_finder = LinkFinder()
        writer = Writer()

        mediator = Mediator(auth_handler, parser, link_finder, writer)

        with driver_setup.setup() as driver:
            mediator.execute(driver)
            logger.info('Script finished successfully.')
    except Exception as e:
        logger.error(f'An error occurred: {e}')


if __name__ == '__main__':
    main()