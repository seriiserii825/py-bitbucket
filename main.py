from rich import print
from classes.Bitbucket import Bitbucket
from classes.Browser import Browser
from classes.Github import Github
from execeptions.BitbucketException import BitbucketException
from modules.git_mirror import git_mirror
from utils import pretty_table


def menu():
    table_header = "Choose an option"
    table_columns = ["Index", "Option"]
    table_rows = [
        ["1", "Git Mirror"],
        ["2", "Repos to File"],
        ["3", "Find Repo in File"],
        ["4", "Create new repo in browser"],
        ["5", "Clone from github"],
    ]
    pretty_table(table_header, table_columns, table_rows)

    choice = input("Enter your choice: ")
    if choice == "1":
        git_mirror()
    elif choice == "2":
        bb = Bitbucket()
        bb.repos_to_file()
        menu()
    elif choice == "3":
        bb = Bitbucket()
        try:
            bb.find_repo_from_file()
        except BitbucketException as e:
            print(f"[red]Error: {e}[/red]")
        menu()
    elif choice == "4":
        bb = Bitbucket()
        try:
            repo_name = bb.new_repo()
            workspace = bb.select_workspace()
            bw = Browser(bb.workspace, repo_name)
            bw.create_repo_in_browser()
            bw.edit_group_in_browser(workspace, repo_name)
        except BitbucketException as e:
            print(f"[red]Error: {e}[/red]")
        menu()
    elif choice == "5":
        gth = Github()
        try:
            gth.clone_repo()
        except Exception as e:
            print(f"[red]Error: {e}[/red]")
    else:
        print("[red]Invalid choice! Please try again.[/red]")
        menu()


if __name__ == "__main__":
    menu()
