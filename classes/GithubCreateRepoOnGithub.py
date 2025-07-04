import os
from classes.GithubClass import GithubClass
from execeptions.GithubException import GithubException
from utils import pretty_print


class GithubCreateRepoOnGithub:
    def __init__(self):
        self.start()

    def start(self):
        self._create_repo_on_github()

    def _create_repo_on_github(self):
        pretty_print("Creating a new repository on GitHub...")
        gth = GithubClass()
        try:
            current_dir = os.getcwd()
            pretty_print(f"Current directory: {current_dir}")
            agree = (
                input(
                    "Do you want to create a repository from the current folder? (yes/no): "
                )
                .strip()
                .lower()
            )
            if agree == "yes":
                gth.create_repo_from_folder()
            else:
                pretty_print("Failed to create a repository. Exiting...", error=True)
                exit()
        except GithubException as e:
            pretty_print(f"Error: {e}", error=True)
