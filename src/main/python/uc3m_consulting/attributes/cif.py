"""CIF attribute validation class"""
from uc3m_consulting.attributes.attributes import Attributes
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class Cif(Attributes):
    """Validates the company CIF"""

    def __init__(self, attr_value: str):
        super().__init__()
        self._error_message = "Invalid CIF format"
        self._validation_pattern = r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$"
        self._attr_value = self._validate(attr_value)

    def _validate(self, value: str) -> str:
        """Validate the CIF format and control character"""
        if not isinstance(value, str):
            raise EnterpriseManagementException("CIF code must be a string")

        super()._validate(value)

        first_letter = value[0]
        number_part = value[1:8]
        control_char = value[8]

        sum_odd_digits = 0
        sum_even_digits = 0

        for i in range(len(number_part)):
            if i % 2 == 0:
                doubled_digit = int(number_part[i]) * 2
                if doubled_digit > 9:
                    sum_odd_digits += (doubled_digit // 10) + (doubled_digit % 10)
                else:
                    sum_odd_digits += doubled_digit
            else:
                sum_even_digits += int(number_part[i])

        total = sum_odd_digits + sum_even_digits
        expected_control_number = 10 - (total % 10)

        if expected_control_number == 10:
            expected_control_number = 0

        control_letter_mapping = "JABCDEFGHI"

        if first_letter in ("A", "B", "E", "H"):
            if str(expected_control_number) != control_char:
                raise EnterpriseManagementException("Invalid CIF character control number")
        elif first_letter in ("P", "Q", "S", "K"):
            if control_letter_mapping[expected_control_number] != control_char:
                raise EnterpriseManagementException("Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")

        return value
