"""Attributes generic class"""
import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class Attributes:
    """Attributes generic class"""
    def __init__(self):
        self._attr_value = ""
        self._error_message = ""
        self._validation_pattern = r""

    def _validate(self, value):
        """Validates the attribute value"""
        my_regex = re.compile(self._validation_pattern)
        res = my_regex.fullmatch(value)
        if not res:
            raise EnterpriseManagementException(self._error_message)
        return value

    @property
    def value(self):
        """Returns the attribute value"""
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        """Sets the attribute value"""
        self._attr_value = attr_value
