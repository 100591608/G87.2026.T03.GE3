"""Projects JSON store"""
from uc3m_consulting.stores.json_store_master import JsonStoreMaster
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import PROJECTS_STORE_FILE


class ProjectsJsonStore(JsonStoreMaster):
    """Class for managing the projects store"""

    def __init__(self):
        super().__init__(PROJECTS_STORE_FILE)

    def add_item_to_store(self, item_to_add):
        self.load_store()
        for project_item in self._data_list:
            if project_item == item_to_add.to_json():
                raise EnterpriseManagementException("Duplicated project in projects list")
        super().add_item_to_store(item_to_add)
