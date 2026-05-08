from rich import print
from classes.BitbucketClone import BitbucketClone
from classes.BitbucketCreateRepo import BitbucketCreateRepo
from classes.BitbucketDeleteRepo import BitbucketDeleteRepo
from classes.BitbucketDeleteRepos import BitbucketDeleteRepos
from classes.BitbucketFindRepoInFile import BitbucketFindRepoInFile
from classes.BitbucketMirror import BitbucketMirror
from classes.BitbucketPlaywrightCreateRepo import BitbucketPlaywrightCreateRepo
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
        ["6", "[red]Delete multiple repos on bitbucket"],
        ["7", "[blue]Clone repo on bitbucket"],
        ["8", "[blue]Set and push new origin bitbucket"],
        ["9", "[green]From github to csv"],
        ["10", "[green]Create repo on github"],
        ["11", "[green]Clone from github"],
        ["12", "[red]Delete repo on github"],
        ["13", "[red]Delete mutliple repos on github"],
        ["14", "[green]From bitbucket to github"],
        ["15", "[green]From github to bitbucket"],
        ["16", "[green]Rename repo on github"],
        ["17", "[green]Rename repo from current folder (auto set-url)"],
        ["18", "[red]Exit"],
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
        # BitbucketCreateRepo()
        BitbucketPlaywrightCreateRepo()
        BitbucketReposToFile()
    elif choice == "5":
        BitbucketDeleteRepo()
        BitbucketReposToFile()
    elif choice == "6":
        BitbucketDeleteRepos()
        BitbucketReposToFile()
    elif choice == "7":
        BitbucketClone()
    elif choice == "8":
        set_origin_url_bitbucket()
    elif choice == "9":
        GithubReposToFile()
    elif choice == "10":
        GithubCreateRepoOnGithub()
        GithubReposToFile()
    elif choice == "11":
        GithubCloneRepo()
    elif choice == "12":
        GithubDeleteRepo()
        GithubReposToFile()
    elif choice == "13":
        GithubDeleteRepos()
        GithubReposToFile()
    elif choice == "14":
        BitbucketToGithub()
        GithubReposToFile()
    elif choice == "15":
        GithubToBitbucket()
        BitbucketReposToFile()
    elif choice == "16":
        GithubRenameRepo()
        GithubReposToFile()
    elif choice == "17":
        GithubRenameRepoFromCwd()
        GithubReposToFile()
    else:
        print("[red]Exiting the program...")
        exit(0)


if __name__ == "__main__":
    menu()
