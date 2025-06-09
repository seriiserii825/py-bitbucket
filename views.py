from classes.Bitbucket import Bitbucket
from classes.Browser import Browser
from classes.Github import Github
from execeptions.BitbucketException import BitbucketException


def repos_to_file():
    bb = Bitbucket()
    bb.repos_to_file()


def find_repo_in_file():
    bb = Bitbucket()
    try:
        bb.find_repo_from_file()
    except BitbucketException as e:
        print(f"[red]Error: {e}[/red]")


def create_new_repo_in_browser():
    bb = Bitbucket()
    try:
        repo_name = bb.new_repo()
        workspace = bb.select_workspace()
        bw = Browser(bb.workspace, repo_name)
        bw.create_repo_in_browser()
        bw.edit_group_in_browser(workspace, repo_name)
    except BitbucketException as e:
        print(f"[red]Error: {e}[/red]")


def clone_from_github():
    gth = Github()
    try:
        gth.clone_repo()
    except Exception as e:
        print(f"[red]Error: {e}[/red]")
