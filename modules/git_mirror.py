import os
import subprocess
import webbrowser

from classes.Browser import Browser
from libs.select import selectOne


def git_mirror():
    repo_name = _get_repo_name()
    workspaces = ["blueline2025", "sites-bludelego", "seriiserii825"]
    workspace = selectOne(workspaces)
    _clone_repo(repo_name, workspace)
    _cd_cloned_repo(repo_name)
    bw = Browser(workspace, repo_name)
    bw.create_repo_in_browser()
    bw.edit_group_in_browser(workspace, repo_name)
    _push_to_new_repo(repo_name)
    _set_new_origin(repo_name)
    _cd_up()
    _success(repo_name)


def _get_repo_name() -> str:
    repo_name = input("Enter repo_name: ")
    if not repo_name:
        print("Repository name cannot be empty.")
        exit(1)
    return repo_name


def _clone_repo(repo_name: str, workspace: str):
    clone_cmd = ["git", "clone", "--mirror",
                 f"git@bitbucket.org:{workspace}/{repo_name}.git"]
    subprocess.run(clone_cmd, check=True)


def _push_to_new_repo(repo_name: str):
    repo_url = f"git@bitbucket.org:blueline-wordpress-sites/{repo_name}.git"
    print(f"repo_url: {repo_url}")
    push_cmd = ["git", "push", "--mirror", repo_url]
    # check_for_errors with raise error
    try:
        subprocess.run(push_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error pushing to new repository: {e}")
        _change_main_barnch_in_browser(repo_name)


def _set_new_origin(repo_name: str):
    remote_url = f"git@bitbucket.org:blueline-wordpress-sites/{repo_name}.git"
    set_url_cmd = ["git", "remote", "set-url", "origin", remote_url]
    try:
        subprocess.run(set_url_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error setting new origin URL: {e}")
        exit(1)


def _cd_up():
    os.chdir("..")
    print("Changed directory to parent.")


def _success(repo_name: str):
    print(
        f"Repository {repo_name} has been\
        cloned and pushed to blueline-wordpress-sites."
    )
    print("Go and delete old repo in blueline2025.")


def _cd_cloned_repo(repo_name: str):
    repo_git_name = f"{repo_name}.git"
    if not os.path.exists(repo_git_name):
        print(f"Repository {repo_git_name} does not exist.")
        exit(1)
    os.chdir(repo_git_name)


def _change_main_barnch_in_browser(repo_name: str):
    print("Change main branch to main in your Bitbucket account.")
    change_url = f"https://bitbucket.org/blueline-wordpress-sites/{repo_name}/admin"
    print(change_url)
    webbrowser.open(change_url)
    confirm = input(
        "Press 'y' when you have changed the main branch to main: ")
    if confirm.lower() != 'y':
        print("Aborting...")
        exit(1)
