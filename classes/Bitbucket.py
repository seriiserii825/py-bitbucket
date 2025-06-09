import csv
import os
from classes.AccountsCsv import AccountsCsv
from classes.BitbucketApi import BitbucketApi
from execeptions.AccountException import AccountException
from pyfzf.pyfzf import FzfPrompt

from my_types.account_type import AccountType
from my_types.repo_type import RepoType
from utils import pretty_print, pretty_table


fzf = FzfPrompt()


class Bitbucket():
    def __init__(self):
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_DIR = os.path.dirname(self.ROOT_DIR)
        self.workspaces: list[str] = []
        self.workspace: str | None = None
        self.account: AccountType | None = None
        self.email: str | None = None
        # self.auth = HTTPBasicAuth(self.username, self.app_password)

    def init_repo_data(self) -> None:
        self._choose_account_by_email()
        if not self.account:
            raise AccountException(
                "Account not selected. Please choose an account first.")
        self._printAccountByAlreadySelectedEmail()
        workspaces = self._get_workspaces_from_api()
        file_name = f"{self.account.email}_repos.csv"
        file_path = os.path.join(self.ROOT_DIR, file_name)
        self._delete_repo_file(file_path)

        with open(file_path, "a") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Workspace"])

        for workspace in workspaces:
            repos: list[RepoType] = self._get_repos_by_workspace(workspace)
            self._repos_to_file(repos)

    def _printAccountByAlreadySelectedEmail(self):
        ac = AccountsCsv()
        ac.print_account_values_by_email(self.email)

    def _choose_account_by_email(self):
        ac = AccountsCsv()
        self.account = ac.choose_account_by_email()
        self.email = self.account.email

    def _get_workspaces_from_api(self) -> list[str]:
        if not self.account:
            raise AccountException(
                "Account not selected. Please choose an account first.")
        ba = BitbucketApi(
            username=self.account.username,
            app_password=self.account.app_password,
        )
        return ba.fetch_workspace_list()

    def _get_repos_by_workspace(self, workspace) -> list[RepoType]:
        if not self.account:
            raise AccountException(
                "Account not selected. Please choose an account first.")
        ba = BitbucketApi(
            username=self.account.username,
            app_password=self.account.app_password,
        )
        return ba.fetch_workspace_repos(workspace)

    def _repos_to_file(self, repos: list[RepoType]) -> None:
        if not self.account:
            raise AccountException(
                "Account not selected. Please choose an account first.")
        file_name = f"{self.account.email}_repos.csv"
        file_path = os.path.join(self.ROOT_DIR, file_name)
        with open(file_path, "a") as f:
            writer = csv.writer(f)
            for repo in repos:
                # Get the repo name from full name
                repo_name = repo.name.split("/")[-1]
                writer.writerow([repo_name, repo.workspace])
        pretty_print(
            f"Repositories saved to {file_path}"
        )

    def _delete_repo_file(self, file_path) -> None:
        if not os.path.exists(file_path):
            pretty_print(f"File {file_path} does not exist.", error=True)
            return
        os.remove(file_path)

    def list_repos(self) -> None:
        if not self.workspaces:
            pretty_print("No repositories found.", error=True)
            return
        table_title = f"Repositories in Workspace: {self.workspace}"
        table_columns = ["Index", "Repository"]
        table_rows = [[str(i), repo]
                      for i, repo in enumerate(self.workspaces, start=1)]
        pretty_table(
            title=table_title,
            columns=table_columns,
            rows=table_rows,
        )


    # def openPermissionsInBrowser(self):
    #     if not self.is_in_new_account:
    #         print("[red]❌ Repository does not exist on the new account. Cannot open permissions in browser.")
    #         return
    #     url = f"https://bitbucket.org/{self.new_workspace}/{self.repo_name}/admin/access"
    #     print(f"Opening permissions page for {self.repo_name} in browser...")
    #     os.system(f"google-chrome-stable {url}")
    #
    # def cloneNewRepo(self):
    #     repo_url = f"git clone git@bitbucket.org:blueline2025/{self.repo_name}.git"
    #     # go to downloads
    #     os.chdir(os.path.expanduser("~/Downloads"))
    #     # clone the new repo
    #     os.system(repo_url)
    #
    # def pushNewRepo(self):
    #     if not self.is_in_old_account:
    #         print("[red]❌ Repository does not exist on the old account. Cannot push to new repository.")
    #         return
    #
    #     old_repo_path = os.path.join(os.path.expanduser("~/Downloads"), self.repo_name + ".git")
    #     os.chdir(old_repo_path)
    #     push_command = f"git push --mirror git@bitbucket.org:blueline2025/{self.repo_name}.git"
    #     print(f"Executing command: {push_command}")
    #     agree = input("Do you want to push the changes to the new repo? (y/n): ")
    #     if agree.lower() != 'y':
    #         print("Push aborted.")
    #         return
    #     os.system(push_command)
    #
