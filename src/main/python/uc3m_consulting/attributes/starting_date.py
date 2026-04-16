"""Starting date attribute validation class"""
from datetime import datetime, timezone
from uc3m_consulting.attributes.attributes import Attributes
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class StartingDate(Attributes):
    """Validates the project starting date"""

    def __init__(self, attr_value: str):
        super().__init__()
        self._error_message = "Invalid date format"
        self._validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        validated_value = self._validate(attr_value)

        try:
            my_date = datetime.strptime(validated_value, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

        if my_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")

        self._attr_value = validated_value
