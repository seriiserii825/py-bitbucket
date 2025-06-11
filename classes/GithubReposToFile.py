from classes.GithubClass import GithubClass
from execeptions.GithubException import GithubException
from utils import pretty_print


class GithubReposToFile:
    def __init__(self):
        pretty_print("Fetching Github Repositories to File")
        self.start()

    def start(self):
        gth = GithubClass()
        try:
            gth.export_github_repos_to_csv()
        except GithubException as e:
            pretty_print(f"Error: {e}", error=True)
