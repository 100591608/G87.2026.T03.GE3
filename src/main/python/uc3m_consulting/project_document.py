"""Contains the class OrderShipping"""
import re
import json
from typing import Any
from datetime import datetime, timezone
import hashlib
from freezegun import freeze_time
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (TEST_DOCUMENTS_STORE_FILE,
                                                       TEST_NUMDOCS_STORE_FILE)
from uc3m_consulting.stores.documents_json_store import DocumentsJsonStore
from uc3m_consulting.stores.num_docs_json_store import NumDocsJsonStore

class ProjectDocument():
    """Class representing the information required for shipping of an order"""

    def __init__(self, project_id: str, file_name):
        self.__alg = "SHA-256"
        self.__type = "PDF"
        self.__project_id = project_id
        self.__file_name = file_name
        justnow = datetime.now(timezone.utc)
        self.__register_date = datetime.timestamp(justnow)

    def to_json(self):
        """returns the object data in json format"""
        return {"alg": self.__alg,
                "type": self.__type,
                "project_id": self.__project_id,
                "file_name": self.__file_name,
                "register_date": self.__register_date,
                "document_signature": self.document_signature}

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + str(self.__alg) +",typ:" + str(self.__type) +",project_id:" + \
               str(self.__project_id) + ",file_name:" + str(self.__file_name) + \
               ",register_date:" + str(self.__register_date) + "}"

    @property
    def project_id(self):
        """Property that represents the product_id of the patient"""
        return self.__project_id

    @project_id.setter
    def project_id(self, value):
        self.__project_id = value

    @property
    def file_name(self):
        """Property that represents the order_id"""
        return self.__file_name
    @file_name.setter
    def file_name(self, value):
        self.__file_name = value

    @property
    def register_date(self):
        """Property that represents the phone number of the client"""
        return self.__register_date
    @register_date.setter
    def register_date(self, value):
        self.__register_date = value


    @property
    def document_signature(self):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @staticmethod
    def read_json_documents() -> Any:
        """Reads the documents json store"""
        try:
            with open(TEST_DOCUMENTS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                document_list = json.load(file)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        return document_list

    @staticmethod
    def read_json_num_docs() -> Any:
        """Reads the num documents json store"""
        try:
            with open(TEST_NUMDOCS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                stored_query_summaries = json.load(file)
        except FileNotFoundError:
            stored_query_summaries = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return stored_query_summaries

    @staticmethod
    def write_json_num_docs(stored_query_summaries):
        """Writes the num documents json store"""
        try:
            with open(TEST_NUMDOCS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(stored_query_summaries, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex

    @classmethod
    def find_docs(cls, date_str):
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
        document_store = DocumentsJsonStore()
        document_list = document_store.load_store()

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
                    project_document = cls(document_item["project_id"], document_item["file_name"])
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

        num_docs_store = NumDocsJsonStore()
        num_docs_store.add_item_to_store(query_summary_data)
        return valid_count
