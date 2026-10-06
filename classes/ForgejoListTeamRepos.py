from classes.ForgejoClass import ForgejoClass
from execeptions.ForgejoException import ForgejoException
from utils import pretty_print


class ForgejoListTeamRepos:
    def __init__(self):
        self.start()

    def start(self):
        pretty_print("Listing repos of a Forgejo team...")
        fj = ForgejoClass()
        try:
            fj.list_team_repos()
        except ForgejoException as e:
            pretty_print(f"Error: {e}", error=True)
