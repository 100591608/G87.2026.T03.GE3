"""File to test singleton pattern"""

from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.stores.projects_json_store import ProjectsJsonStore
from uc3m_consulting.stores.num_docs_json_store import NumDocsJsonStore
from uc3m_consulting.stores.documents_json_store import DocumentsJsonStore

enterprise_manager_1 = EnterpriseManager()
enterprise_manager_2 = EnterpriseManager()
print(enterprise_manager_1 == enterprise_manager_2)

project_document_1 = ProjectsJsonStore()
project_document_2 = ProjectsJsonStore()
print(project_document_1 == project_document_2)

num_docs_1 = NumDocsJsonStore()
num_docs_2 = NumDocsJsonStore()
print(num_docs_1 == num_docs_2)

document_1 = DocumentsJsonStore()
document_2 = DocumentsJsonStore()
print(document_1 == document_2)
