from typing import List
from simple_term_menu import TerminalMenu
from rich.console import Console
from rich.table import Table
from rich import print

from classes.Select import Select


def selectOne(options: List[str]) -> str:
    """
    Displays a terminal menu for selecting one option from a list.
    """
    terminal_menu = TerminalMenu(options)
    # menu_entry_index = terminal_menu.show()
    menu_entry_index = terminal_menu.show()
    return options[menu_entry_index]


# selectOne(getThemes())


def selectMultiple(options: List[str]) -> List[str]:
    sl = Select()
    return sl.select_with_fzf(options)
    # """
    # Displays a terminal menu for selecting multiple options from a list.
    # """
    # terminal_menu = TerminalMenu(options,
    #                              multi_select=True,
    #                              show_multi_select_hint=True,
    #                              show_search_hint=True,
    #                              preview_command="bat --color=always {}", preview_size=0.75
    #                              )
    # menu_entry_indices = terminal_menu.show()
    # # print(menu_entry_indices)
    # # print(terminal_menu.chosen_menu_entries)
    # return terminal_menu.chosen_menu_entries


def pretty_print(value, error=False):
    """
    Prints a value in a formatted way, with different colors for error and success.
    """
    if error:
        print("[red]===============================")
        print(f"[red]{value}")
        print("[red]===============================")
    else:
        print("[green]===============================")
        print(f"[green]{value}")
        print("[green]===============================")


def pretty_table(title: str, columns: List[str], rows: List[List[str]]):
    table = Table(title=title)

    for column in columns:
        table.add_column(column, style="white")

    for row in rows:
        table.add_row(*row)

    console = Console()
    console.print(table)
