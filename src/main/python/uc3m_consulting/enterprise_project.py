"""MODULE: enterprise_project. Contains the EnterpriseProject class"""
import re
import hashlib
import json
from typing import Any
from datetime import datetime, timezone
from uc3m_consulting.attributes.acronym import Acronym
from uc3m_consulting.attributes.department import Department
from uc3m_consulting.attributes.description import Description
from uc3m_consulting.attributes.budget import Budget
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import PROJECTS_STORE_FILE

class EnterpriseProject:
    """Class representing a project"""
    #pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(self,
                 company_cif: str,
                 project_acronym: str,
                 project_description: str,
                 department: str,
                 starting_date: str,
                 project_budget: float):
        self.__company_cif = company_cif
        self.__project_description = Description(project_description).value
        self.__project_achronym = Acronym(project_acronym).value
        self.__department = Department(department).value
        self.__starting_date = self.validate_starting_date(starting_date)
        self.__project_budget = Budget(project_budget).value
        justnow = datetime.now(timezone.utc)
        self.__time_stamp = datetime.timestamp(justnow)

    def __str__(self):
        return "Project:" + json.dumps(self.__dict__)

    def to_json(self):
        """returns the object information in json format"""
        return {
            "company_cif": self.__company_cif,
            "project_description": self.__project_description,
            "project_acronym": self.__project_achronym,
            "project_budget": self.__project_budget,
            "department": self.__department,
            "starting_date": self.__starting_date,
            "time_stamp": self.__time_stamp,
            "project_id": self.project_id
        }
    @property
    def company_cif(self):
        """Company's cif"""
        return self.__company_cif

    @company_cif.setter
    def company_cif(self, value):
        self.__company_cif = value

    @property
    def project_description(self):
        """Property representing the project description"""
        return self.__project_description

    @project_description.setter
    def project_description(self, value):
        self.__project_description = value

    @property
    def project_acronym(self):
        """Property representing the acronym"""
        return self.__project_achronym
    @project_acronym.setter
    def project_acronym(self, value):
        self.__project_achronym = value

    @property
    def project_budget(self):
        """Property respresenting the project budget"""
        return self.__project_budget
    @project_budget.setter
    def project_budget(self, value):
        self.__project_budget = value

    @property
    def department(self):
        """Property representing the department"""
        return self.__department
    @department.setter
    def department(self, value):
        self.__department = value

    @property
    def starting_date( self ):
        """Property representing the project's date"""
        return self.__starting_date
    @starting_date.setter
    def starting_date( self, value ):
        self.__starting_date = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def project_id(self):
        """Returns the md5 signature (project id)"""
        return hashlib.md5(str(self).encode()).hexdigest()

    def validate_starting_date(self, target_date):
        """validates the  date format  using regex"""
        date_pattern = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        is_match = date_pattern.fullmatch(target_date)
        if not is_match:
            raise EnterpriseManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(target_date, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

        if my_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")
        return target_date

    @staticmethod
    def read_json_project() -> Any:
        """Reads the projects json store"""
        try:
            with open(PROJECTS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                project_list = json.load(file)
        except FileNotFoundError:
            project_list = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return project_list

    @staticmethod
    def write_json_project(project_list):
        """Writes the projects json store"""
        try:
            with open(PROJECTS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(project_list, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
