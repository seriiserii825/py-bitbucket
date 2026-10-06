from classes.ForgejoClass import ForgejoClass
from execeptions.ForgejoException import ForgejoException
from utils import pretty_print


class ForgejoFindRepo:
    def __init__(self):
        self.start()

    def start(self):
        pretty_print("Find a Forgejo repo and show its teams...")
        fj = ForgejoClass()
        try:
            fj.find_repo()
        except ForgejoException as e:
            pretty_print(f"Error: {e}", error=True)
