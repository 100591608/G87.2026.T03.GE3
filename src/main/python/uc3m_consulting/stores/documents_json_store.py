"""Documents JSON store"""
from uc3m_consulting.stores.json_store_master import JsonStoreMaster
from uc3m_consulting.enterprise_manager_config import TEST_DOCUMENTS_STORE_FILE


class DocumentsJsonStore(JsonStoreMaster):
    """Class for managing the documents store"""

    def __init__(self):
        super().__init__(TEST_DOCUMENTS_STORE_FILE)
