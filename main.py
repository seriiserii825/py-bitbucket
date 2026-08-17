from rich import print
from classes.BitbucketClone import BitbucketClone
from classes.BitbucketCreateRepo import BitbucketCreateRepo
from classes.BitbucketDeleteRepo import BitbucketDeleteRepo
from classes.BitbucketDeleteRepos import BitbucketDeleteRepos
from classes.BitbucketFindRepoInFile import BitbucketFindRepoInFile
from classes.BitbucketMirror import BitbucketMirror
from classes.BitbucketPlaywrightMirror import BitbucketPlaywrightMirror
from classes.BitbucketPlaywrightCreateRepo import BitbucketPlaywrightCreateRepo
from classes.BitbucketReposToFile import BitbucketReposToFile
from classes.BitbucketToGithub import BitbucketToGithub
from classes.GithubToBitbucket import GithubToBitbucket
from classes.GithubCloneRepo import GithubCloneRepo
from classes.GithubCreateRepoOnGithub import GithubCreateRepoOnGithub
from classes.GithubDeleteRepo import GithubDeleteRepo
from classes.GithubDeleteRepos import GithubDeleteRepos
from classes.BitbucketCopyRemoteUrl import BitbucketCopyRemoteUrl
from classes.GithubCopyRemoteUrl import GithubCopyRemoteUrl
from classes.GithubRenameRepoFromCwd import GithubRenameRepoFromCwd
from classes.GithubReposToFile import GithubReposToFile
from utils import pretty_table


def confirm_repo_already_created(destination: str, create_option: str) -> bool:
    print(f"[yellow]Have you already created the new repo on {destination}?")
    print(
        f"[yellow]You can create a repo on {destination} from this script "
        f"(option {create_option} in the main menu)."
    )
    answer = input("Continue with migration? (y/n): ").strip().lower()
    if answer == "y":
        return True
    print(f"[yellow]Redirecting to the main menu so you can create the repo on {destination} first...")
    return False


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
        ["8", "[blue]Copy/set/add remote origin URL (Bitbucket) to clipboard"],
        ["9", "[green]From github to csv"],
        ["10", "[green]Create repo on github"],
        ["11", "[green]Clone from github"],
        ["12", "[red]Delete repo on github"],
        ["13", "[red]Delete mutliple repos on github"],
        ["14", "[green]From bitbucket to github"],
        ["15", "[green]From github to bitbucket"],
        ["16", "[green]Rename repo on github (from current folder, checks folder matches repo)"],
        ["17", "[green]Copy/set/add remote origin URL (GitHub) to clipboard"],
        ["18", "[red]Exit"],
    ]
    pretty_table(table_header, table_columns, table_rows)

    choice = input("Enter your choice: ")
    if choice == "1":
        BitbucketReposToFile()
        menu()
    elif choice == "2":
        BitbucketPlaywrightMirror()
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
        BitbucketCopyRemoteUrl()
        menu()
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
        if confirm_repo_already_created("GitHub", "10"):
            BitbucketToGithub()
            GithubReposToFile()
        else:
            menu()
    elif choice == "15":
        if confirm_repo_already_created("Bitbucket", "4"):
            GithubToBitbucket()
            BitbucketReposToFile()
        else:
            menu()
    elif choice == "16":
        GithubRenameRepoFromCwd()
        GithubReposToFile()
    elif choice == "17":
        GithubCopyRemoteUrl()
        menu()
    else:
        print("[red]Exiting the program...")
        exit(0)


if __name__ == "__main__":
    menu()
