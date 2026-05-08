from classes.AccountsCsv import AccountsCsv
from classes.Bitbucket import Bitbucket
from classes.BitbucketApi import BitbucketApi
from execeptions.BitbucketApiException import BitbucketApiException
from utils import pretty_print


class BitbucketDeleteRepos:
    def __init__(self):
        self.start()

    def start(self):
        repos = self._get_repos()
        if not repos:
            return
        account = AccountsCsv().choose_account_by_email()
        bb_api = BitbucketApi(account.username, account.app_password)
        for repo in repos:
            self._delete_repo(bb_api, repo.name, repo.workspace)

    def _get_repos(self):
        pretty_print("Select repos to delete")
        bb = Bitbucket()
        return bb.get_repos_from_file_multiple()

    def _delete_repo(self, bb_api: BitbucketApi, repo_name: str, workspace: str):
        pretty_print(f"Deleting: {repo_name} / {workspace}")
        try:
            bb_api.delete_repo_on_bitbucket(repo_name, workspace)
        except BitbucketApiException as e:
            pretty_print(f"Error deleting {repo_name}: {e}", error=True)
