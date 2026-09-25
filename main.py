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
from py_libs.Select import Select


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


def migrate_to_github():
    if confirm_repo_already_created("GitHub", "Create repo on github"):
        BitbucketToGithub()
        GithubReposToFile()
    else:
        menu()


def migrate_to_bitbucket():
    if confirm_repo_already_created("Bitbucket", "Create new repo on bitbucket"):
        GithubToBitbucket()
        BitbucketReposToFile()
    else:
        menu()


def menu():
    # (label, action, return to menu after action)
    options = [
        ("Bitbucket repos to File", BitbucketReposToFile, True),
        ("Clone and Mirror Bitbucket Repo to Bitbucket",
         lambda: (BitbucketPlaywrightMirror(), BitbucketReposToFile()), False),
        ("Find Repo in bitbucket File", BitbucketFindRepoInFile, True),
        ("Create new repo on bitbucket",
         lambda: (BitbucketPlaywrightCreateRepo(), BitbucketReposToFile()), False),
        ("Delete repo on bitbucket",
         lambda: (BitbucketDeleteRepo(), BitbucketReposToFile()), False),
        ("Delete multiple repos on bitbucket",
         lambda: (BitbucketDeleteRepos(), BitbucketReposToFile()), False),
        ("Clone repo on bitbucket", BitbucketClone, False),
        ("Copy/set/add remote origin URL (Bitbucket) to clipboard",
         BitbucketCopyRemoteUrl, True),
        ("From github to csv", GithubReposToFile, False),
        ("Create repo on github",
         lambda: (GithubCreateRepoOnGithub(), GithubReposToFile()), False),
        ("Clone from github", GithubCloneRepo, False),
        ("Delete repo on github",
         lambda: (GithubDeleteRepo(), GithubReposToFile()), False),
        ("Delete mutliple repos on github",
         lambda: (GithubDeleteRepos(), GithubReposToFile()), False),
        ("From bitbucket to github", migrate_to_github, False),
        ("From github to bitbucket", migrate_to_bitbucket, False),
        ("Rename repo on github (from current folder, checks folder matches repo)",
         lambda: (GithubRenameRepoFromCwd(), GithubReposToFile()), False),
        ("Copy/set/add remote origin URL (GitHub) to clipboard",
         GithubCopyRemoteUrl, True),
        ("Exit", None, False),
    ]
    labels = [label for label, _, _ in options]
    choice = Select.select_fzf_one(labels)
    if choice is None or choice not in labels:
        print("[red]Exiting the program...")
        exit(0)
    _, action, back_to_menu = options[labels.index(choice)]
    if action is None:
        print("[red]Exiting the program...")
        exit(0)
    action()
    if back_to_menu:
        menu()


if __name__ == "__main__":
    menu()
