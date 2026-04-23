"""Module for the NumDocsDocument class"""
import re
from datetime import datetime, timezone
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class NumDocsDocument:
    """Class representing the result of find_docs"""

    def __init__(self, query_date: str, num_files: int):
        self.__query_date = self.validate_query_date(query_date)
        self.__report_date = datetime.now(timezone.utc).timestamp()
        self.__num_files = num_files

    @staticmethod
    def validate_query_date(date_str: str) -> str:
        """Validates the input date"""
        date_pattern = re.compile(r"^(([0-2]\d|3[0-1])/(0\d|1[0-2])/\d\d\d\d)$")
        is_match = date_pattern.fullmatch(date_str)
        if not is_match:
            raise EnterpriseManagementException("Invalid date format")

        try:
            datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

        return date_str

    def to_json(self):
        """Returns the object information in json format"""
        return {
            "Querydate": self.__query_date,
            "ReportDate": self.__report_date,
            "Numfiles": self.__num_files
        }

    @property
    def query_date(self):
        """Getter for query_date"""
        return self.__query_date

    @property
    def report_date(self):
        """Getter for report_date"""
        return self.__report_date

    @property
    def num_files(self):
        """Getter for num_files"""
        return self.__num_files
