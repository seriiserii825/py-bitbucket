from classes.ForgejoClass import ForgejoClass
from execeptions.ForgejoException import ForgejoException
from utils import pretty_print


class ForgejoCloneRepo:
    def __init__(self):
        self.start()

    def start(self):
        pretty_print("Cloning a repository from Forgejo...")
        fj = ForgejoClass()
        try:
            fj.clone_repo()
        except ForgejoException as e:
            pretty_print(f"Error: {e}", error=True)
