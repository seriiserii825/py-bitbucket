from classes.GithubClass import GithubClass
from execeptions.GithubException import GithubException
from utils import pretty_print


class GithubTogglePrivate:
    def __init__(self):
        self.start()

    def start(self):
        gth = GithubClass()
        try:
            gth.toggle_private()
        except GithubException as e:
            pretty_print(f"Error: {e}", error=True)
