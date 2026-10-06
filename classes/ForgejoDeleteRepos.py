from classes.ForgejoClass import ForgejoClass
from execeptions.ForgejoException import ForgejoException
from utils import pretty_print


class ForgejoDeleteRepos:
    def __init__(self):
        self.start()

    def start(self):
        pretty_print("Deleting multiple repositories on Forgejo...")
        fj = ForgejoClass()
        try:
            fj.delete_repos()
        except ForgejoException as e:
            pretty_print(f"Error: {e}", error=True)
