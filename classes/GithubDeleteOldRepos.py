from classes.GithubClass import GithubClass
from execeptions.GithubException import GithubException
from utils import pretty_print


class GithubDeleteOldRepos:
    def __init__(self):
        self.start()

    def start(self):
        self.delete_old_repos()

    def delete_old_repos(self):
        gth = GithubClass()
        try:
            gth.delete_old_repos()
        except GithubException as e:
            pretty_print(f"Error: {e}", error=True)
