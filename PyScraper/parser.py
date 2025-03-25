from typing import List, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from logs import logger
from student import Student



class Parser:
    def parse(self, driver: WebDriver, url: str) -> List[Student]:
        logger.info(f'Parsing students from the URL: {url}.')
        driver.get(url)

        html_students = driver.find_elements(By.XPATH, "//tbody/tr")
        if not html_students:
            logger.warning(f'Cannot find <tr> tags in the <tbody>. URL: {url}')
            return []

        students = [
            student for html_student in html_students
            if (student := self.deserialize_html_student(html_student, url))
        ]

        logger.info(f'Found {len(students)} students.')
        return students

    def deserialize_html_student(self, html_student: WebElement, url: str) -> Optional[Student]:
        tds = html_student.find_elements(By.TAG_NAME, 'td')
        if not tds:
            logger.warning(f'Cannot find <td> tags in the <tr>. URL: {url}')
            return None

        if len(tds) < 5:
            logger.warning(
                f'Invalid <td> structure. Expected 5 elements, '
                f'but found {len(tds)}. URL: {url}'
            )
            return None

        return Student(
            name=tds[1].text.strip() or "N/A",
            record_book_id=tds[2].text.strip() or "N/A",
            group_id=tds[3].text.strip() or "N/A",
            specialty_id=tds[4].text.strip() or "N/A"
        )