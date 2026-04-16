"""Department attribute validation class"""
from uc3m_consulting.attributes.attributes import Attributes

class Department(Attributes):
    """Validates the project department"""

    def __init__(self, attr_value: str):
        super().__init__()
        self._error_message = "Invalid department"
        self._validation_pattern = r"^(HR|FINANCE|LEGAL|LOGISTICS)"
        self._attr_value = self._validate(attr_value)
