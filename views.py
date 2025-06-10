from classes.Bitbucket import Bitbucket
from classes.Browser import Browser
from classes.GithubClass import GithubClass
from execeptions.BitbucketException import BitbucketException
from execeptions.GithubException import GithubException
from utils import pretty_print


def repos_to_file():
    bb = Bitbucket()
    bb.repos_to_file()


def find_repo_in_file():
    bb = Bitbucket()
    try:
        bb.get_repo_from_file()
    except BitbucketException as e:
        pretty_print(f"Error: {e}", error=True)


def create_new_repo_in_bitbucket():
    bb = Bitbucket()
    try:
        repo_name = bb.new_repo()
        workspace = bb.select_workspace()
        bw = Browser(bb.workspace, repo_name)
        bw.create_repo_in_browser()
        bw.edit_group_in_browser(workspace, repo_name)
    except BitbucketException as e:
        pretty_print(f"Error: {e}", error=True)


def clone_from_github():
    gth = GithubClass()
    try:
        gth.clone_repo()
    except Exception as e:
        pretty_print(f"Error: {e}", error=True)


def create_repo_on_github():
    gth = GithubClass()
    try:
        gth.create_repo_from_folder()
    except GithubException as e:
        pretty_print(f"Error: {e}", error=True)


def delete_reop_on_github():
    gth = GithubClass()
    try:
        gth.delete_repo()
    except GithubException as e:
        pretty_print(f"Error: {e}", error=True)

def delete_repos_on_github():
    gth = GithubClass()
    try:
        gth.delete_repos()
    except GithubException as e:
        pretty_print(f"Error: {e}", error=True)


def from_bitbucket_to_github():
    gth = GithubClass()
    try:
        repo_name = gth.clone_mirror_from_bitbucket()
        repo_exists_on_github = gth.check_repo_on_github(repo_name)
        if repo_exists_on_github:
            raise GithubException(
                f"Repository {repo_name} already exists on GitHub."
            )
        gth.create_repo_by_arg(repo_name)
        gth.push_mirror_to_github(repo_name)
    except GithubException as e:
        pretty_print(f"Error: {e}", error=True)


def export_github_repos_to_csv():
    gth = GithubClass()
    try:
        gth.export_github_repos_to_csv()
    except GithubException as e:
        pretty_print(f"Error: {e}", error=True)
