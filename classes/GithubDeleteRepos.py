from classes.GithubClass import GithubClass
from execeptions.GithubException import GithubException
from utils import pretty_print


class GithubDeleteRepos:
    def start(self):
        self.delete_repos()

    def delete_repos(self):
        gth = GithubClass()
        try:
            gth.delete_repos()
        except GithubException as e:
            pretty_print(f"Error: {e}", error=True)
