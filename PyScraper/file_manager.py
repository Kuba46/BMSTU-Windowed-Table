from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options

from logs import logger, OUTPUT_FILE_NAME
from student import Student, HEADERS

import csv

class FileManager(object):
    def deserialize_html_student(html_student: WebElement, url: str) -> Optional[Student]:
        tds = html_student.find_elements(By.TAG_NAME, 'td')
        if not tds:
            logger.warning(f'Cannot find <td> tags in the <tr>. URL: {url}')
            return None

        # Current HTML structure contains at least 5 <td> elements in the <tr>.
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


    def parse_students(driver: WebDriver, url: str) -> list[Student]:
        logger.info(f'Parsing students from the URL: {url}.')
        driver.get(url)

        html_students = driver.find_elements(By.XPATH, "//tbody/tr")
        if not html_students:
            logger.warning(f'Cannot find <tr> tags in the <tbody>. URL: {url}')
            return []

        students = [
            student for html_student in html_students
            if (student := FileManager.deserialize_html_student(html_student, url))
        ]

        logger.info(f'Found {len(students)} students.')
        return students


    def find_department_links(driver: WebDriver) -> list[str]:
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


    def write_to_csv(writer: csv.DictWriter, students: list[Student]):
        logger.info('Writing students to the CSV file.')
        for student in students:
            writer.writerow(student.to_dict())
        logger.info(f'Wrote {len(students)} students to the CSV file.')


    def setup_driver() -> WebDriver:
        chrome_options = Options()
        # Comment this if you want to see the browser.
        chrome_options.add_argument('--headless')
        return webdriver.Chrome(options=chrome_options)

    def process_students(driver: WebDriver, links: list[str]):
        with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=HEADERS)
            writer.writeheader()
            for link in links:
                students = FileManager.parse_students(driver, link)
                FileManager.write_to_csv(writer, students)

