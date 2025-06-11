from classes.GithubClass import GithubClass
from execeptions.GithubException import GithubException
from utils import pretty_print


class GithubDeleteRepo:
    def __init__(self):
        self.start()

    def start(self):
        self.delete_reop_on_github()

    def delete_reop_on_github(self):
        pretty_print("Deleting a repository on GitHub...")
        gth = GithubClass()
        try:
            gth.delete_repo()
        except GithubException as e:
            pretty_print(f"Error: {e}", error=True)
