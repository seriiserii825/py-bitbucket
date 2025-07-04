from classes.AccountsCsv import AccountsCsv
from classes.Bitbucket import Bitbucket
from classes.BitbucketApi import BitbucketApi
from execeptions.BitbucketApiException import BitbucketApiException
from my_types.repo_type import RepoType
from utils import pretty_print


class BitbucketDeleteRepo:
    def __init__(self):
        self.start()

    def start(self):
        repo, workpsace = self._get_repo()
        self._delete_repo(repo, workpsace)

    def _get_repo(self) -> RepoType:
        pretty_print("Select a repo from file")
        bb = Bitbucket()
        name, workspace = bb.get_repo_from_file()
        return RepoType(name=name, workspace=workspace)

    def _delete_repo(self, repo_name: str, workspace: str):
        pretty_print(f"Deleting repository: {repo_name} in workspace: {workspace}")
        ac = AccountsCsv()
        account = ac.choose_account_by_email()
        bb_api = BitbucketApi(account.username, account.app_password)
        try:
            bb_api.delete_repo_on_bitbucket(repo_name, workspace)
        except BitbucketApiException as e:
            pretty_print(f"Error deleting repository: {e}", error=True)
