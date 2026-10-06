from classes.ForgejoClass import ForgejoClass
from execeptions.ForgejoException import ForgejoException
from utils import pretty_print


class ForgejoCreateTeam:
    def __init__(self):
        self.start()

    def start(self):
        pretty_print("Creating a new team in the Forgejo organization...")
        fj = ForgejoClass()
        try:
            fj.create_team()
        except ForgejoException as e:
            pretty_print(f"Error: {e}", error=True)
