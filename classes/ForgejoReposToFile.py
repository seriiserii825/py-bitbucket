from classes.ForgejoClass import ForgejoClass
from execeptions.ForgejoException import ForgejoException
from utils import pretty_print


class ForgejoReposToFile:
    def __init__(self):
        self.start()

    def start(self):
        pretty_print("Fetching Forgejo repositories to file")
        fj = ForgejoClass()
        try:
            fj.export_repos_to_csv()
        except ForgejoException as e:
            pretty_print(f"Error: {e}", error=True)
