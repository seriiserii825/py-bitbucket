from classes.ForgejoClass import ForgejoClass
from execeptions.ForgejoException import ForgejoException
from utils import pretty_print


class ForgejoCreateRepo:
    def __init__(self):
        self.start()

    def start(self):
        pretty_print("Creating a new repository on Forgejo...")
        fj = ForgejoClass()
        try:
            fj.create_repo_from_folder()
        except ForgejoException as e:
            pretty_print(f"Error: {e}", error=True)
