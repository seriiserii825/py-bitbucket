from classes.GithubClass import GithubClass
from utils import pretty_print


class GithubCloneRepo:
    def __init__(self):
        self.start()

    def start(self):
        self._clone_repo()

    def _clone_repo(self):
        gth = GithubClass()
        try:
            gth.clone_repo()
        except Exception as e:
            pretty_print(f"Error: {e}", error=True)
