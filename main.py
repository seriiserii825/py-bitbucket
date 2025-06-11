from rich import print
from classes.BitbucketCreateRepo import BitbucketCreateRepo
from classes.BitbucketFindRepoInFile import BitbucketFindRepoInFile
from classes.BitbucketMirror import BitbucketMirror
from classes.BitbucketReposToFile import BitbucketReposToFile
from utils import pretty_table
from views import clone_from_bitbucket, clone_from_github
from views import create_repo_on_github, delete_repos_on_github
from views import delete_reop_on_github, set_origin_url_bitbucket
from views import export_github_repos_to_csv, from_bitbucket_to_github
from views import create_new_repo_in_bitbucket


def menu():
    table_header = "Choose an option"
    table_columns = ["Index", "Option"]
    table_rows = [
        ["1", "[blue]Bitbucket repos to File"],
        ["2", "[blue]Clone and Mirror Bitbucket Repo to Bitbucket"],
        ["3", "[blue]Find Repo in bitbucket File"],
        ["4", "[blue]Create new repo on bitbucket"],
        ["5", "[blue]Clone repo on bitbucket"],
        ["6", "[blue]Set and push new origin bitbucket"],
        ["7", "[green]Clone from github"],
        ["8", "[green]Create repo on github"],
        ["9", "[red]Delete repo on github"],
        ["10", "[red]Delete mutliple repos on github"],
        ["11", "[green]From bitbucket to github"],
        ["12", "[green]From github to csv"],
        ["13", "[red]Exit"]
    ]
    pretty_table(table_header, table_columns, table_rows)

    choice = input("Enter your choice: ")
    if choice == "1":
        bb = BitbucketReposToFile()
        bb.start()
        menu()
    elif choice == "2":
        bm = BitbucketMirror()
        bm.start()
    elif choice == "3":
        bb = BitbucketFindRepoInFile()
        bb.start()
        menu()
    elif choice == "4":
        bb = BitbucketCreateRepo()
        bb.start()
        menu()
    elif choice == "5":
        clone_from_bitbucket()
    elif choice == "6":
        set_origin_url_bitbucket()
    elif choice == "7":
        clone_from_github()
    elif choice == "8":
        create_repo_on_github()
    elif choice == "9":
        delete_reop_on_github()
    elif choice == "10":
        delete_repos_on_github()
    elif choice == "11":
        from_bitbucket_to_github()
    elif choice == "12":
        export_github_repos_to_csv()
    else:
        print("[red]Exiting the program...")
        exit(0)


if __name__ == "__main__":
    menu()
