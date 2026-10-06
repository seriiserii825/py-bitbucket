from classes.ForgejoClass import ForgejoClass
from execeptions.ForgejoException import ForgejoException
from modules.git_mirror import clone_mirror_from_bitbucket
from utils import pretty_print


class BitbucketToForgejo:
    def __init__(self):
        self.start()

    def start(self):
        pretty_print("Starting migration from Bitbucket to Forgejo...")
        fj = ForgejoClass()
        try:
            # clones the mirror and cd's into <repo>.git
            repo_name, _ = clone_mirror_from_bitbucket()
            full_name = fj.create_repo_by_arg(repo_name)
            fj.push_mirror(full_name)
        except ForgejoException as e:
            pretty_print(f"Error: {e}", error=True)
