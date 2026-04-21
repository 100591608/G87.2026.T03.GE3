"""Generic JSON store class"""
import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class JsonStoreMaster:
    """Superclass for managing storage in JSON files"""

    def __init__(self, file_store):
        self._data_list = []
        self._file_name = file_store
        self.load_store()

    def load_store(self):
        """Loads the JSON file"""
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return self._data_list

    def save_store(self):
        """Saves the JSON file"""
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex

    def add_item_to_store(self, item_to_add):
        """Adds an item to the store"""
        self.load_store()
        self._data_list.append(item_to_add.to_json())
        self.save_store()
