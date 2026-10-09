import os
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


def choose_repo_name() -> tuple[str, bool]:
    """
    Asks whether to take the repo name from the current folder or to type it.
    Returns (repo_name, from_folder).
    """
    folder_name = os.path.basename(os.getcwd())
    from_folder_option = f"From current folder: {folder_name}"
    choice = selectOne([from_folder_option, "Enter name manually"])
    if choice == from_folder_option:
        return folder_name, True
    repo_name = input("Enter the repository name: ").strip()
    if not repo_name:
        raise ValueError("Repository name cannot be empty.")
    return repo_name, False


def confirm_push_current_folder(from_folder: bool) -> bool:
    """
    Repo named after the current folder: push it as before.
    Manually named repo: ask, since the current folder may be unrelated.
    """
    if from_folder:
        return True
    prompt = f"Init and push current folder '{os.getcwd()}' to the new repo?"
    answer = input(f"{prompt} (y/n): ").strip().lower()
    return answer == "y"
