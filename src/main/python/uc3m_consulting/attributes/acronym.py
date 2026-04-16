"""Acronym attribute validation class"""
from uc3m_consulting.attributes.attributes import Attributes

class Acronym(Attributes):
    """Validates the project acronym"""

    def __init__(self, attr_value: str):
        super().__init__()
        self._error_message = "Invalid acronym"
        self._validation_pattern = r"^[a-zA-Z0-9]{5,10}"
        self._attr_value = self._validate(attr_value)
