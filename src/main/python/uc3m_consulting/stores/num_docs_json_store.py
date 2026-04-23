"""NumDocs JSON store"""
from uc3m_consulting.stores.json_store_master import JsonStoreMaster
from uc3m_consulting.enterprise_manager_config import TEST_NUMDOCS_STORE_FILE


class NumDocsJsonStore(JsonStoreMaster):
    """Class for managing the num docs store"""

    def __init__(self):
        super().__init__(TEST_NUMDOCS_STORE_FILE)
