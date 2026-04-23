"""NumDocs JSON store"""
from uc3m_consulting.stores.json_store_master import JsonStoreMaster
from uc3m_consulting.enterprise_manager_config import TEST_NUMDOCS_STORE_FILE


class NumDocsJsonStore(JsonStoreMaster):
    """Class for managing the num docs store"""

    class __NumDocsJsonStore(JsonStoreMaster):
        """Class for managing the num docs store"""

        def __init__(self):
            super().__init__(TEST_NUMDOCS_STORE_FILE)

    instance = None

    def __new__(cls):
        if not NumDocsJsonStore.instance:
            NumDocsJsonStore.instance = NumDocsJsonStore.__NumDocsJsonStore()
        return NumDocsJsonStore.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
