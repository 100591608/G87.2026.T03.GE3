"""Attributes generic class"""
import re
from uc3m_consulting import EnterpriseManagementException

class Attributes():
    """Attributes generic class"""
    def __init__(self):
        self.__attr_value = ""
        self.__error_message = ""
        self._validation_pattern = r""

    def _validate(self, value):
        """Validates the attribute value"""
        my_regex = re.compile(self._validation_pattern)
        res = my_regex.fullmatch(value)
        if not res:
            raise EnterpriseManagementException(self.__error_message)
        return value

    @property
    def value(self):
        """Returns the attribute value"""
        return self.__attr_value

    @value.setter
    def value(self, attr_value):
        """Sets the attribute value"""
        self.__attr_value = attr_value
