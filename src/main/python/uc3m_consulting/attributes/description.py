"""Description attribute validation class"""
from uc3m_consulting.attributes.attributes import Attributes


class Description(Attributes):
    """Validates the project description"""

    def __init__(self, attr_value: str):
        super().__init__()
        self._error_message = "Invalid description format"
        self._validation_pattern = r"^.{10,30}"
        self._attr_value = self._validate(attr_value)