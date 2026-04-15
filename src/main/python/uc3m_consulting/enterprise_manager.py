"""Module """
import re
import json

from datetime import datetime, timezone
from typing import Any

from freezegun import freeze_time
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (PROJECTS_STORE_FILE,
                                                       TEST_DOCUMENTS_STORE_FILE,
                                                       TEST_NUMDOCS_STORE_FILE)
from uc3m_consulting.project_document import ProjectDocument

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif_number: str):
        """validates a cif number """
        if not isinstance(cif_number, str):
            raise EnterpriseManagementException("CIF code must be a string")
        cif_pattern = re.compile(r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$")
        if not cif_pattern.fullmatch(cif_number):
            raise EnterpriseManagementException("Invalid CIF format")

        first_letter = cif_number[0]
        number_part = cif_number[1:8]
        control_char = cif_number[8]

        sum_odd_digits = 0
        sum_even_digits = 0

        for i in range(len(number_part)):
            if i % 2 == 0:
                doubled_digit = int(number_part[i]) * 2
                if doubled_digit > 9:
                    sum_odd_digits = sum_odd_digits + (doubled_digit // 10) + (doubled_digit % 10)
                else:
                    sum_odd_digits = sum_odd_digits + doubled_digit
            else:
                sum_even_digits = sum_even_digits + int(number_part[i])

        total = sum_odd_digits + sum_even_digits
        last_digit_of_sum = total % 10
        expected_control_number = 10 - last_digit_of_sum

        if expected_control_number == 10:
            expected_control_number = 0

        control_letter_mapping = "JABCDEFGHI"

        if first_letter in ('A', 'B', 'E', 'H'):
            if str(expected_control_number) != control_char:
                raise EnterpriseManagementException("Invalid CIF character control number")
        elif first_letter in ('P', 'Q', 'S', 'K'):
            if control_letter_mapping[expected_control_number] != control_char:
                raise EnterpriseManagementException("Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")
        return True

    #pylint: disable=too-many-arguments, too-many-positional-arguments
    def register_project(self,
                         company_cif: str,
                         project_acronym: str,
                         project_description: str,
                         department: str,
                         date: str,
                         budget: str):
        """registers a new project"""
        self.validate_cif(company_cif)

        new_project = EnterpriseProject(company_cif=company_cif,
                                        project_acronym=project_acronym,
                                        project_description=project_description,
                                        department=department,
                                        starting_date=date,
                                        project_budget=budget)

        project_list = self.read_json_project()

        for project_item in project_list:
            if project_item == new_project.to_json():
                raise EnterpriseManagementException("Duplicated project in projects list")

        project_list.append(new_project.to_json())

        self.write_json_project(project_list)
        return new_project.project_id

    def write_json_project(self, project_list):
        try:
            with open(PROJECTS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(project_list, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def read_json_project(self) -> Any:
        try:
            with open(PROJECTS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                project_list = json.load(file)
        except FileNotFoundError:
            project_list = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return project_list

    def find_docs(self, date_str):
        """
        Generates a JSON report counting valid documents for a specific date.

        Checks cryptographic hashes and timestamps to ensure historical data integrity.
        Saves the output to 'resultado.json'.

        Args:
            date_str (str): date to query.

        Returns:
            number of documents found if report is successfully generated and saved.

        Raises:
            EnterpriseManagementException: On invalid date, file IO errors,
                missing data, or cryptographic integrity failure.
        """
        date_pattern = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        is_match = date_pattern.fullmatch(date_str)
        if not is_match:
            raise EnterpriseManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex


        # open documents
        document_list = self.read_json_documents()


        valid_count = 0

        # loop to find
        for document_item in document_list:
            time_val = document_item["register_date"]

            # string conversion for easy match
            doc_date_str = datetime.fromtimestamp(time_val).strftime("%d/%m/%Y")

            if doc_date_str == date_str:
                doc_registration_time = datetime.fromtimestamp(time_val, tz=timezone.utc)
                with freeze_time(doc_registration_time):
                    # check the project id (thanks to freezetime)
                    # if project_id are different then the data has been
                    #manipulated
                    project_document = ProjectDocument(document_item["project_id"], document_item["file_name"])
                    if project_document.document_signature == document_item["document_signature"]:
                        valid_count = valid_count + 1
                    else:
                        raise EnterpriseManagementException("Inconsistent document signature")

        if valid_count == 0:
            raise EnterpriseManagementException("No documents found")
        # prepare json text
        now_str = datetime.now(timezone.utc).timestamp()
        query_summary_data = {"Querydate":  date_str,
             "ReportDate": now_str,
             "Numfiles": valid_count
             }

        stored_query_summaries = self.read_json_num_docs()
        stored_query_summaries.append(query_summary_data)
        self.write_json_num_docs(stored_query_summaries)
        return valid_count

    def write_json_num_docs(self, stored_query_summaries):
        try:
            with open(TEST_NUMDOCS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(stored_query_summaries, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex

    def read_json_documents(self) -> Any:
        try:
            with open(TEST_DOCUMENTS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                document_list = json.load(file)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        return document_list

    def read_json_num_docs(self) -> Any:
        try:
            with open(TEST_NUMDOCS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                stored_query_summaries = json.load(file)
        except FileNotFoundError:
            stored_query_summaries = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return stored_query_summaries
