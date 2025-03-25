from dataclasses import dataclass, fields
from selenium.webdriver.remote.webdriver import WebDriver


@dataclass
class Student:
    name: str
    record_book_id: str
    group_id: str
    specialty_id: str

    FIELDS_MAPPING = {
        'name': 'Full Name',
        'record_book_id': 'Record Book ID',
        'group_id': 'Group ID',
        'specialty_id': 'Specialty ID'
    }

    def to_dict(self):
        return {
            self.FIELDS_MAPPING[field.name]: getattr(self, field.name)
            for field in fields(self)
        }


HEADERS = [
    Student.FIELDS_MAPPING[field.name] for field in fields(Student)
]
