from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from logs import logger


class LinkFinder:
    def find_links(self, driver: WebDriver) -> List[str]:
        logger.info('Finding department links.')
        first_ul = driver.find_element(By.XPATH, "//ul[@class='eu-tree-nodeset']")
        links = first_ul.find_elements(
            By.XPATH,
            (
                "./li[normalize-space(@class)='eu-tree-closed']"
                "/ul/li[normalize-space(@class)='eu-tree-closed']"
                "/ul/li[@class='eu-tree-active']/a"
            ),
        )
        if not links:
            raise ValueError(
                f'Cannot find department <a> tag in the document. '
                f'URL: {driver.current_url}'
            )

        logger.info(f'Found {len(links)} department links.')
        return [elem for link in links if (elem := link.get_attribute('href'))]
