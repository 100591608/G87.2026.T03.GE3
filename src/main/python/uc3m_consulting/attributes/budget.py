"""Budget attribute validation class"""
from uc3m_consulting.attributes.attributes import Attributes
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class Budget(Attributes):
    """Validates the project budget"""

    def __init__(self, attr_value):
        super().__init__()

        try:
            budget_float = float(attr_value)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc

        budget_string = str(budget_float)
        if "." in budget_string:
            decimals = len(budget_string.split(".")[1])
            if decimals > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if budget_float < 50000 or budget_float > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")

        self._attr_value = attr_value
