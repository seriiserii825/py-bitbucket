from rich import print
from classes.Bitbucket import Bitbucket
from modules.git_mirror import git_mirror
from utils import pretty_table


def menu():
    table_header = "Choose an option"
    table_columns = ["Index", "Option"]
    table_rows = [
        ["1", "Git Mirror"],
        ["2", "Move Repo to Bitbucket"]
    ]
    pretty_table(table_header, table_columns, table_rows)

    choice = input("Enter your choice: ")
    if choice == "1":
        git_mirror()
    elif choice == "2":
        bb = Bitbucket()
        bb.init_repo_data()
    else:
        print("[red]Invalid choice! Please try again.[/red]")
        menu()

if __name__ == "__main__":
    menu()
