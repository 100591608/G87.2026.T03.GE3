"""Module """
from datetime import datetime
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.stores.projects_json_store import ProjectsJsonStore
from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.num_docs_document import NumDocsDocument
from uc3m_consulting.stores.documents_json_store import DocumentsJsonStore
from uc3m_consulting.stores.num_docs_json_store import NumDocsJsonStore

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""

    class __EnterpriseManager:
        """Class for providing the methods for managing the orders"""
        def __init__(self):
            pass

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

        #pylint: disable=too-many-locals
        def find_docs(self, date_str):
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
            NumDocsDocument.validate_query_date(date_str)

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
                    ProjectDocument.get_docs_from_file(document_item)
                    valid_count = valid_count + 1

            if valid_count == 0:
                raise EnterpriseManagementException("No documents found")
            # prepare json text
            my_num_docs = NumDocsDocument(date_str, valid_count)

            num_docs_store = NumDocsJsonStore()
            num_docs_store.add_item_to_store(my_num_docs)
            return valid_count

    instance = None

    def __new__(cls):
        if not EnterpriseManager.instance:
            EnterpriseManager.instance = EnterpriseManager.__EnterpriseManager()
        return EnterpriseManager.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
