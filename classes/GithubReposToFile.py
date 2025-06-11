from classes.GithubClass import GithubClass
from execeptions.GithubException import GithubException
from utils import pretty_print


class GithubReposToFile:
    def start(self):
        gth = GithubClass()
        try:
            gth.export_github_repos_to_csv()
        except GithubException as e:
            pretty_print(f"Error: {e}", error=True)
