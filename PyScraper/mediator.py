from typing import List
from selenium.webdriver.remote.webdriver import WebDriver

from logs import OUTPUT_FILE_NAME
from student import HEADERS
import csv


class Mediator:
    def __init__(self, auth_handler, parser, link_finder, writer):
        self.auth_handler = auth_handler
        self.parser = parser
        self.link_finder = link_finder
        self.writer = writer

    def execute(self, driver: WebDriver):
        self.auth_handler.authenticate(driver)
        links = self.link_finder.find_links(driver)
        self.process_students(driver, links)

    def process_students(self, driver: WebDriver, links: List[str]):
        with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=HEADERS)
            writer.writeheader()
            for link in links:
                students = self.parser.parse(driver, link)
                self.writer.write(writer, students)