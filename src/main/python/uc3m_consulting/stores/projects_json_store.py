"""Projects JSON store"""
from uc3m_consulting.stores.json_store_master import JsonStoreMaster
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import PROJECTS_STORE_FILE


class ProjectsJsonStore(JsonStoreMaster):
    """Class for managing the projects store"""

    class __ProjectsJsonStore(JsonStoreMaster):
        """Class for managing the projects store"""

        def __init__(self):
            super().__init__(PROJECTS_STORE_FILE)

        def add_item_to_store(self, item_to_add):
            self.load_store()
            for project_item in self._data_list:
                if project_item == item_to_add.to_json():
                    raise EnterpriseManagementException("Duplicated project in projects list")
            super().add_item_to_store(item_to_add)

    instance = None

    def __new__(cls):
        if not ProjectsJsonStore.instance:
            ProjectsJsonStore.instance = ProjectsJsonStore.__ProjectsJsonStore()
        return ProjectsJsonStore.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
