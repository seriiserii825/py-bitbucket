from rich import print
from modules.git_mirror import git_mirror
from utils import pretty_table
from views import clone_from_github, create_repo_on_github
from views import delete_reop_on_github
from views import export_github_repos_to_csv, from_bitbucket_to_github
from views import create_new_repo_in_bitbucket, find_repo_in_file, repos_to_file


def menu():
    table_header = "Choose an option"
    table_columns = ["Index", "Option"]
    table_rows = [
        ["1", "Git Mirror"],
        ["2", "Bitbucket repos to File"],
        ["3", "Find Repo in File"],
        ["4", "Create new repo on bitbucket"],
        ["5", "Clone from github"],
        ["6", "Create repo on github"],
        ["7", "Delete repo on github"],
        ["8", "From bitbucket to github"],
        ["9", "From github to csv"]
    ]
    pretty_table(table_header, table_columns, table_rows)

    choice = input("Enter your choice: ")
    if choice == "1":
        git_mirror()
    elif choice == "2":
        repos_to_file()
        menu()
    elif choice == "3":
        find_repo_in_file()
        menu()
    elif choice == "4":
        create_new_repo_in_bitbucket()
        menu()
    elif choice == "5":
        clone_from_github()
    elif choice == "6":
        create_repo_on_github()
    elif choice == "7":
        delete_reop_on_github()
    elif choice == "8":
        from_bitbucket_to_github()
    elif choice == "9":
        export_github_repos_to_csv()
    else:
        print("[red]Invalid choice! Please try again.")
        menu()


if __name__ == "__main__":
    menu()
