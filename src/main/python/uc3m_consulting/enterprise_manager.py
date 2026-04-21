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
from uc3m_consulting.stores.projects_json_store import ProjectsJsonStore

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
        new_project = EnterpriseProject(company_cif=company_cif,
                                        project_acronym=project_acronym,
                                        project_description=project_description,
                                        department=department,
                                        starting_date=date,
                                        project_budget=budget)

        project_store = ProjectsJsonStore()
        project_store.add_item_to_store(new_project)
        return new_project.project_id
