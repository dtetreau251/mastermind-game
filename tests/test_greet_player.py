import unittest
from unittest.mock import patch
from ..game import greet_player


@patch("builtins.print")
def test_print_mastermind(mock_print):
    # The actual test
    greet_player("John")
    mock_print.assert_called_with("Hello ", "John")
    greet_player("Eric")
    mock_print.assert_called_with("Hello ", "Eric")

    # Showing what is in mock
    import sys

    sys.stdout.write(str(mock_print.call_args) + "\n")
    sys.stdout.write(str(mock_print.call_args_list) + "\n")


# def test_get_numbers_check_status_code_equals_200():
#     response = requests.get(
#         "https://www.random.org/integers?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new"
#     )
#     assert response.status_code == 200


# def test_get_string():
#     response = requests.get(
#         "https://www.random.org/integers?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new"
#     )
#     assert type(response.text) == "str"
