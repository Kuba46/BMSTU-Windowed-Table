from file_manager import FileManager
from logs import logger, LOGIN_URL
from mediator import Mediator


def main():
    try:
        logger.info('Starting the script.')
        with FileManager.setup_driver() as driver:
            Mediator.auth(driver, LOGIN_URL)
            links = FileManager.find_department_links(driver)
            FileManager.process_students(driver, links)
            logger.info('Script finished successfully.')
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    main()
