import csv
import os
from classes.AccountsCsv import AccountsCsv
from classes.BitbucketApi import BitbucketApi
from execeptions.AccountException import AccountException
from pyfzf.pyfzf import FzfPrompt

from execeptions.BitbucketException import BitbucketException
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

    def repos_to_file(self) -> None:
        account = self._choose_account_by_email()
        if not self.account:
            raise AccountException(
                "Account not selected. Please choose an account first.")
        self._printAccountByEmail(account.email)
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

    def _printAccountByEmail(self, email):
        ac = AccountsCsv()
        ac.print_account_values_by_email(email)

    def _choose_account_by_email(self) -> AccountType:
        return self._get_account_from_file()

    def _get_account_from_file(self) -> AccountType:
        ac = AccountsCsv()
        return ac.choose_account_by_email()

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

    def find_repo_from_file(self):
        repos = self._get_repos_from_file()
        repos_for_fzf = [f"{repo.name} ({repo.workspace})" for repo in repos]
        selected_repo = fzf.prompt(repos_for_fzf)
        print(f"selected_repo: {selected_repo[0]}")

    def _get_repos_from_file(self) -> list[RepoType]:
        account = self._choose_account_by_email()
        file_name = f"{account.email}_repos.csv"
        file_path = os.path.join(self.ROOT_DIR, file_name)
        repos = []
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                repos.append(RepoType(name=row[0], workspace=row[1]))
        return repos

    def _get_workspaces_from_file(self) -> list[str]:
        repos = self._get_repos_from_file()
        workspaces = set(repo.workspace for repo in repos)
        return list(workspaces)

    def select_workspace(self) -> str:
        workspaces = self._get_workspaces_from_file()
        if not workspaces:
            raise BitbucketException("No workspaces found.")
        workspace = fzf.prompt(workspaces)
        return workspace

    def new_repo(self):
        account = self._choose_account_by_email()
        bb_api = BitbucketApi(account.username, account.app_password)
        repo_name = input("Enter the new repository name: ")
        if not repo_name:
            raise BitbucketException("Repository name cannot be empty.")

        new_repo = bb_api._createRepoOnBitbucketApi(
            workspace=self.workspace,
            project_key=self.workspace,
            repo_name=repo_name
        )
        if new_repo.status_code in (200, 201):
            print(
                f"[green]✅ Repository '{repo_name}' created successfully!")
            self.is_in_new_account = True
            return repo_name
        else:
            raise BitbucketException(
                f"Failed to create repository '{repo_name}'. "
                f"Status code: {new_repo.status_code}"
            )
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
