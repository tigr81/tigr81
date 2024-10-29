import tigr81.utils as tigr81_utils


def test_pretty_list_empty():
    """Test for an empty list."""
    result = tigr81_utils.pretty_list([])
    assert result == "Empty"

def test_pretty_list_single():
    """Test for a list with a single item."""
    result = tigr81_utils.pretty_list(["apple"])
    assert result == "apple"

def test_pretty_list_two_items():
    """Test for a list with two items."""
    result = tigr81_utils.pretty_list(["apple", "banana"])
    assert result == "apple and banana"

def test_pretty_list_multiple_items():
    """Test for a list with multiple items."""
    result = tigr81_utils.pretty_list(["apple", "banana", "cherry"])
    assert result == "apple, banana and cherry"

def test_pretty_list_long_list():
    """Test for a longer list of items."""
    result = tigr81_utils.pretty_list(["apple", "banana", "cherry", "date"])
    assert result == "apple, banana, cherry and date"

def test_pretty_list_numbers():
    """Test for a list containing numbers as strings."""
    result = tigr81_utils.pretty_list(["1", "2", "3"])
    assert result == "1, 2 and 3"

def test_pretty_list_special_characters():
    """Test for a list with special characters."""
    result = tigr81_utils.pretty_list(["apple", "banana", "!@#$%^&*()"])
    assert result == "apple, banana and !@#$%^&*()"
