from typing import List

from py_libs.Menu import Menu
from py_libs.Print import Print
from py_libs.Select import Select


def selectOne(options: List[str]) -> str:
    """
    Displays a terminal menu for selecting one option from a list.
    """
    return Select.select_one(options)


def selectMultiple(options: List[str]) -> List[str]:
    return Select.select_with_fzf(options)


def pretty_print(value, error=False):
    """
    Prints a value in a formatted way, with different colors for error and success.
    """
    if error:
        Print.error(value)
    else:
        Print.success(value)


def pretty_table(title: str, columns: List[str], rows: List[List[str]]):
    Menu.display(title, columns, rows)
