import enum


class StrEnum(str, enum.Enum):
    """A base class for string-based enumerations.

    This class combines the functionality of str and enum.Enum,
    allowing the creation of enumerations where each member
    is a string. The string representation of each member is its value.

    Example:
        class Color(StrEnum):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"

        print(Color.RED)  # Output: red
    """

    def __repr__(self) -> str:
        """Return the string representation of the enum member."""
        return self.value

    def __str__(self) -> str:
        """Return the string representation of the enum member."""
        return self.value
