from typing import List

from logs import logger
from student import Student
import csv


class Writer:
    def write(self, writer: csv.DictWriter, students: List[Student]):
        logger.info('Writing students to the CSV file.')
        for student in students:
            writer.writerow(student.to_dict())
        logger.info(f'Wrote {len(students)} students to the CSV file.')
