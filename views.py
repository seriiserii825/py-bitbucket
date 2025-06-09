from classes.Bitbucket import Bitbucket
from classes.Browser import Browser
from classes.Github import Github
from execeptions.BitbucketException import BitbucketException
from execeptions.GithubException import GithubException


def repos_to_file():
    bb = Bitbucket()
    bb.repos_to_file()


def find_repo_in_file():
    bb = Bitbucket()
    try:
        bb.find_repo_from_file()
    except BitbucketException as e:
        print(f"[red]Error: {e}[/red]")


def create_new_repo_in_bitbucket():
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


def create_repo_on_github():
    gth = Github()
    try:
        gth.create_repo_from_folder()
    except GithubException as e:
        print(f"[red]Error: {e}[/red]")


def delete_reop_on_github():
    gth = Github()
    try:
        gth.delete_repo()
    except GithubException as e:
        print(f"[red]Error: {e}[/red]")


def from_bitbucket_to_github():
    gth = Github()
    try:
        repo_name = gth.clone_mirror_from_bitbucket()
        gth.create_repo_by_arg(repo_name)
        gth.push_mirror_to_github(repo_name)
    except GithubException as e:
        print(f"[red]Error: {e}[/red]")
