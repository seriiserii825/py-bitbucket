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
from py_libs.Menu import Menu


def confirm_repo_already_created(destination: str) -> bool:
    print(f"[yellow]Have you already created the new repo on {destination}?")
    print(
        f"[yellow]You can create a repo on {destination} from this script "
        f"(\"Create repo\" in the {destination} menu)."
    )
    answer = input("Continue with migration? (y/n): ").strip().lower()
    if answer == "y":
        return True
    print(f"[yellow]Back to the {destination} menu so you can create the repo first...")
    return False


def migrate_to_github() -> bool:
    if not confirm_repo_already_created("GitHub"):
        return False
    BitbucketToGithub()
    GithubReposToFile()
    return True


def migrate_to_bitbucket() -> bool:
    if not confirm_repo_already_created("Bitbucket"):
        return False
    GithubToBitbucket()
    BitbucketReposToFile()
    return True


def exit_program():
    print("[red]Exiting the program...")
    exit(0)


def run_menu(title: str, options) -> None:
    """
    options: list of (label, action, return to this menu after action).
    action None means "Back" (return to the caller).
    An action returning False also returns to this menu.
    """
    while True:
        rows = [[str(i), label] for i, (label, _, _) in enumerate(options)]
        Menu.display(title, ["#", "Option"], rows)
        _, action, back_to_menu = options[Menu.choose_option()]
        if action is None:
            return
        result = action()
        if not back_to_menu and result is not False:
            exit(0)


def bitbucket_menu():
    run_menu("Bitbucket", [
        ("[blue]Bitbucket repos to File", BitbucketReposToFile, True),
        ("[blue]Clone and Mirror Bitbucket Repo to Bitbucket",
         lambda: (BitbucketPlaywrightMirror(), BitbucketReposToFile()), False),
        ("[blue]Find Repo in bitbucket File", BitbucketFindRepoInFile, True),
        ("[blue]Create new repo on bitbucket",
         lambda: (BitbucketPlaywrightCreateRepo(), BitbucketReposToFile()), False),
        ("[blue]Delete repo on bitbucket",
         lambda: (BitbucketDeleteRepo(), BitbucketReposToFile()), False),
        ("[red]Delete multiple repos on bitbucket",
         lambda: (BitbucketDeleteRepos(), BitbucketReposToFile()), False),
        ("[blue]Clone repo on bitbucket", BitbucketClone, False),
        ("[blue]Copy/set/add remote origin URL (Bitbucket) to clipboard",
         BitbucketCopyRemoteUrl, True),
        ("[blue]From github to bitbucket", migrate_to_bitbucket, False),
        ("[yellow]Back", None, False),
        ("[red]Exit", exit_program, False),
    ])


def github_menu():
    run_menu("GitHub", [
        ("[green]From github to csv", GithubReposToFile, False),
        ("[green]Create repo on github",
         lambda: (GithubCreateRepoOnGithub(), GithubReposToFile()), False),
        ("[green]Clone from github", GithubCloneRepo, False),
        ("[red]Delete repo on github",
         lambda: (GithubDeleteRepo(), GithubReposToFile()), False),
        ("[red]Delete mutliple repos on github",
         lambda: (GithubDeleteRepos(), GithubReposToFile()), False),
        ("[green]From bitbucket to github", migrate_to_github, False),
        ("[green]Rename repo on github (from current folder, checks folder matches repo)",
         lambda: (GithubRenameRepoFromCwd(), GithubReposToFile()), False),
        ("[green]Copy/set/add remote origin URL (GitHub) to clipboard",
         GithubCopyRemoteUrl, True),
        ("[yellow]Back", None, False),
        ("[red]Exit", exit_program, False),
    ])


def menu():
    run_menu("Main menu", [
        ("[green]GitHub", github_menu, True),
        ("[blue]Bitbucket", bitbucket_menu, True),
        ("[red]Exit", exit_program, False),
    ])


if __name__ == "__main__":
    menu()
