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
            gth.create_repo_from_folder()
        except GithubException as e:
            pretty_print(f"Error: {e}", error=True)
