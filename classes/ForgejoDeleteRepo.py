from classes.ForgejoClass import ForgejoClass
from execeptions.ForgejoException import ForgejoException
from utils import pretty_print


class ForgejoDeleteRepo:
    def __init__(self):
        self.start()

    def start(self):
        pretty_print("Deleting a repository on Forgejo...")
        fj = ForgejoClass()
        try:
            fj.delete_repo()
        except ForgejoException as e:
            pretty_print(f"Error: {e}", error=True)
