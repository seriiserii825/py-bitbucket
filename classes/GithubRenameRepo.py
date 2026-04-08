from classes.GithubClass import GithubClass
from execeptions.GithubException import GithubException
from utils import pretty_print


class GithubRenameRepo:
    def __init__(self):
        self.start()

    def start(self):
        gth = GithubClass()
        try:
            gth.rename_repo()
        except GithubException as e:
            pretty_print(f"Error: {e}", error=True)
