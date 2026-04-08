from rich import print
from classes.BitbucketClone import BitbucketClone
from classes.BitbucketCreateRepo import BitbucketCreateRepo
from classes.BitbucketDeleteRepo import BitbucketDeleteRepo
from classes.BitbucketFindRepoInFile import BitbucketFindRepoInFile
from classes.BitbucketMirror import BitbucketMirror
from classes.BitbucketReposToFile import BitbucketReposToFile
from classes.BitbucketToGithub import BitbucketToGithub
from classes.GithubToBitbucket import GithubToBitbucket
from classes.GithubCloneRepo import GithubCloneRepo
from classes.GithubCreateRepoOnGithub import GithubCreateRepoOnGithub
from classes.GithubDeleteRepo import GithubDeleteRepo
from classes.GithubDeleteRepos import GithubDeleteRepos
from classes.GithubRenameRepo import GithubRenameRepo
from classes.GithubRenameRepoFromCwd import GithubRenameRepoFromCwd
from classes.GithubReposToFile import GithubReposToFile
from utils import pretty_table
from views import set_origin_url_bitbucket


def menu():
    table_header = "Choose an option"
    table_columns = ["Index", "Option"]
    table_rows = [
        ["1", "[blue]Bitbucket repos to File"],
        ["2", "[blue]Clone and Mirror Bitbucket Repo to Bitbucket"],
        ["3", "[blue]Find Repo in bitbucket File"],
        ["4", "[blue]Create new repo on bitbucket"],
        ["5", "[blue]Delete repo on bitbucket"],
        ["6", "[blue]Clone repo on bitbucket"],
        ["7", "[blue]Set and push new origin bitbucket"],
        ["8", "[green]From github to csv"],
        ["9", "[green]Create repo on github"],
        ["10", "[green]Clone from github"],
        ["11", "[red]Delete repo on github"],
        ["12", "[red]Delete mutliple repos on github"],
        ["13", "[green]From bitbucket to github"],
        ["14", "[green]From github to bitbucket"],
        ["15", "[green]Rename repo on github"],
        ["16", "[green]Rename repo from current folder (auto set-url)"],
        ["17", "[red]Exit"],
    ]
    pretty_table(table_header, table_columns, table_rows)

    choice = input("Enter your choice: ")
    if choice == "1":
        BitbucketReposToFile()
        menu()
    elif choice == "2":
        BitbucketMirror()
        BitbucketReposToFile()
    elif choice == "3":
        BitbucketFindRepoInFile()
        menu()
    elif choice == "3":
        BitbucketFindRepoInFile()
        menu()
    elif choice == "4":
        BitbucketCreateRepo()
        BitbucketReposToFile()
    elif choice == "5":
        BitbucketDeleteRepo()
        BitbucketReposToFile()
    elif choice == "6":
        BitbucketClone()
    elif choice == "7":
        set_origin_url_bitbucket()
    elif choice == "8":
        GithubReposToFile()
    elif choice == "9":
        GithubCreateRepoOnGithub()
        GithubReposToFile()
    elif choice == "10":
        GithubCloneRepo()
    elif choice == "11":
        GithubDeleteRepo()
        GithubReposToFile()
    elif choice == "12":
        GithubDeleteRepos()
        GithubReposToFile()
    elif choice == "13":
        BitbucketToGithub()
        GithubReposToFile()
    elif choice == "14":
        GithubToBitbucket()
        BitbucketReposToFile()
    elif choice == "15":
        GithubRenameRepo()
        GithubReposToFile()
    elif choice == "16":
        GithubRenameRepoFromCwd()
        GithubReposToFile()
    else:
        print("[red]Exiting the program...")
        exit(0)


if __name__ == "__main__":
    menu()
