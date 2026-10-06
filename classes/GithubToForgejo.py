import os
import subprocess

from pyfzf.pyfzf import FzfPrompt

from classes.ForgejoClass import ForgejoClass
from classes.GithubClass import GithubClass
from execeptions.ForgejoException import ForgejoException
from execeptions.GithubException import GithubException
from utils import pretty_print

fzf = FzfPrompt()


class GithubToForgejo:
    def __init__(self):
        self.start()

    def start(self):
        pretty_print("Starting migration from GitHub to Forgejo...")
        fj = ForgejoClass()
        try:
            repo_name = self._clone_mirror_from_github()
            os.chdir(f"{repo_name}.git")
            full_name = fj.create_repo_by_arg(repo_name)
            fj.push_mirror(full_name)
        except (ForgejoException, GithubException) as e:
            pretty_print(f"Error: {e}", error=True)

    def _clone_mirror_from_github(self) -> str:
        gh = GithubClass()
        selected = fzf.prompt(gh._get_repos_from_file())
        if not selected:
            raise ForgejoException("No GitHub repository selected.")
        repo_name = selected[0]
        repo_git_name = f"{repo_name}.git"
        if os.path.exists(repo_git_name):
            print(f"Directory '{repo_git_name}' already exists, skipping clone.")
            return repo_name
        username = gh._get_data_from_env("GITHUB_USERNAME")
        clone_url = f"git@github.com:{username}/{repo_name}.git"
        print(f"command: git clone --mirror {clone_url}")
        result = subprocess.run(["git", "clone", "--mirror", clone_url])
        if result.returncode != 0:
            raise ForgejoException(f"Failed to clone repository '{repo_name}' from GitHub.")
        return repo_name
