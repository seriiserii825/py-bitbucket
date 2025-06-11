from classes.Bitbucket import Bitbucket
from my_types.repo_type import RepoType
from utils import pretty_print


class BitbucketClone:
    def __init__(self):
        self.start()

    def start(self):
        pretty_print("Starting Bitbucket Clone process...")
        name, workspace = self.get_repo_from_file()
        self.clone_repo(name, workspace)

    def get_repo_from_file(self) -> RepoType:
        pretty_print("Retrieving repository details from file...")
        bb = Bitbucket()
        name, workspace = bb.get_repo_from_file()
        return RepoType(name=name, workspace=workspace)

    def clone_repo(self, name: str, workspace: str):
        pretty_print(f"Cloning repository {name} from workspace {workspace}...")
        bb = Bitbucket()
        bb.clone_repo(name, workspace)
        print(f"Repository {name} has been cloned from Bitbucket.")
