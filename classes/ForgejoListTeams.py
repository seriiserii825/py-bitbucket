from classes.ForgejoClass import ForgejoClass
from execeptions.ForgejoException import ForgejoException
from utils import pretty_print


class ForgejoListTeams:
    def __init__(self):
        self.start()

    def start(self):
        pretty_print("Listing teams of the Forgejo organization...")
        fj = ForgejoClass()
        try:
            fj.list_teams()
        except ForgejoException as e:
            pretty_print(f"Error: {e}", error=True)
