import csv
import os
import subprocess
from typing import List
from classes.AccountsCsv import AccountsCsv
from classes.BitbucketApi import BitbucketApi
from execeptions.AccountException import AccountException
from pyfzf.pyfzf import FzfPrompt

from execeptions.BitbucketException import BitbucketException
from my_types.account_type import AccountType
from my_types.repo_type import RepoType
from utils import pretty_print, pretty_table, selectOne


fzf = FzfPrompt()


class Bitbucket:
    def __init__(self) -> None:
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_DIR = os.path.dirname(self.ROOT_DIR)
        self.workspaces: List[str] = []
        self.workspace: str | None = None
        self.account: AccountType | None = None
        self.email: str | None = None

    def clone_repo(self, repo_name: str, workspace: str, mirror: bool = False) -> None:
        if mirror:
            command = f"git clone --mirror \
            git@bitbucket.org:{workspace}/{repo_name}.git"
        else:
            command = f"git clone git@bitbucket.org:{workspace}/{repo_name}.git"
        print(f"command: {command}")
        os.system(command)

    def repos_to_file(self) -> None:
        account = self._choose_account_by_email()
        print(f"account: {account}")

        if not account:
            raise AccountException(
                "Account not selected. Please choose an account first."
            )
        self._printAccountByEmail(account.email)
        workspaces = self._get_workspaces_from_api(account)
        file_name = f"{account.email}_repos.csv"
        file_path = os.path.join(self.ROOT_DIR, file_name)
        self._delete_repo_file(file_path)

        with open(file_path, "a") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Workspace"])

        for workspace in workspaces:
            repos: List[RepoType] = self._get_repos_by_workspace(workspace, account)
            self._repos_to_file(repos, account)

    def _printAccountByEmail(self, email):
        ac = AccountsCsv()
        ac.print_account_values_by_email(email)

    def _choose_account_by_email(self) -> AccountType:
        return self._get_account_from_file()

    def set_new_origin(self) -> None:
        pass
        # repo_name = repo_from_file.split("/")[0]
        # workspace = repo_from_file.split("/")[1]
        # remote_url = f"git@bitbucket.org:{workspace}/{repo_name}.git"
        # set_url_cmd = ["git", "remote", "set-url", "origin", remote_url]
        # try:
        #     subprocess.run(set_url_cmd, check=True)
        # except subprocess.CalledProcessError as e:
        #     raise BitbucketException(
        #         f"Failed to set new origin URL: {e}"
        #     ) from e
        # try:
        #     self.push_origin_force(workspace, repo_name)
        # except BitbucketException as e:
        #     raise BitbucketException(
        #         f"Failed to push to origin after setting new URL: {e}"
        #     ) from e

    def push_origin_force(self, workspace: str, repo_name: str) -> None:
        remote_url = f"git@bitbucket.org:{workspace}/{repo_name}.git"
        push_cmd = ["git", "push -u", "origin main", "--force", remote_url]
        try:
            subprocess.run(push_cmd, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            raise BitbucketException(f"Failed to push to origin: {e}") from e

    def push_to_mirror_repo(self, repo_name: str, workspace: str) -> None:
        repo_url = f"git@bitbucket.org:{workspace}/{repo_name}.git"
        command = f"git push --mirror {repo_url}"
        try:
            subprocess.run(command, check=True, shell=True)
        except Exception as e:
            raise BitbucketException(f"Error pushing to new repository: {e}")

    def set_mirror_origin(self, repo_name: str, workspace: str) -> None:
        remote_url = f"git@bitbucket.org:{workspace}/{repo_name}.git"
        set_url_cmd = ["git", "remote", "set-url", "origin", remote_url]
        try:
            subprocess.run(set_url_cmd, check=True)
        except subprocess.CalledProcessError:
            raise BitbucketException(f"Failed to set new origin URL: {set_url_cmd}")

    def _get_account_from_file(self) -> AccountType:
        ac = AccountsCsv()
        return ac.choose_account_by_email()

    def _get_workspaces_from_api(self, account: AccountType) -> List[str]:
        ba = BitbucketApi(
            username=account.username,
            app_password=account.app_password,
        )
        return ba.fetch_workspace_list()

    def _get_repos_by_workspace(self, workspace, account) -> List[RepoType]:
        ba = BitbucketApi(
            username=account.username,
            app_password=account.app_password,
        )
        return ba.fetch_workspace_repos(workspace)

    def _repos_to_file(self, repos: List[RepoType], account) -> None:
        file_name = f"{account.email}_repos.csv"
        file_path = os.path.join(self.ROOT_DIR, file_name)
        with open(file_path, "a") as f:
            writer = csv.writer(f)
            for repo in repos:
                # Get the repo name from full name
                repo_name = repo.name.split("/")[-1]
                writer.writerow([repo_name, repo.workspace])
        pretty_print(f"Repositories saved to {file_path}")

    def _delete_repo_file(self, file_path) -> None:
        if not os.path.exists(file_path):
            pretty_print(f"File {file_path} does not exist.", error=True)
            return
        os.remove(file_path)

    def get_repo_from_file(self) -> RepoType:
        repos = self._get_repos_from_file()
        sorted_repos = sorted(repos, key=lambda x: (x.workspace, x.name))
        repos_for_fzf = [f"{repo.name}/{repo.workspace}" for repo in sorted_repos]
        selected_repo = fzf.prompt(repos_for_fzf)
        return RepoType(
            name=selected_repo[0].split("/")[0],
            workspace=selected_repo[0].split("/")[1],
        )

    def find_repo_in_file(self):
        repo_name = input("Enter the repository name to search: ")
        if not repo_name:
            raise BitbucketException("Repository name cannot be empty.")
        repos = self._get_repos_from_file()
        finded_repos = [repo for repo in repos if repo_name in repo.name]
        if finded_repos:
            table_title = "Repos"
            table_columns = ["Name", "Workspace"]
            table_rows = [[repo.name, repo.workspace] for repo in finded_repos]
            pretty_table(table_title, table_columns, table_rows)
        else:
            raise BitbucketException(f"Repository '{repo_name}' not found in file.")

    def check_repo_and_workspace_in_file(self, repo_name, workspace) -> bool:
        repos = self._get_repos_from_file()
        return any(
            repo.name == repo_name and repo.workspace == workspace for repo in repos
        )

    def _get_repos_from_file(self) -> List[RepoType]:
        print("Choose an account by email, to search in file:")
        account = self._choose_account_by_email()
        file_name = f"{account.email}_repos.csv"
        file_path = os.path.join(self.ROOT_DIR, file_name)
        repos = []
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                repos.append(RepoType(name=row[0], workspace=row[1]))
        return repos

    def _get_workspaces_from_file(self) -> List[str]:
        repos = self._get_repos_from_file()
        workspaces = set(repo.workspace for repo in repos)
        return list(workspaces)

    def select_workspace(self) -> str:
        workspaces = self._get_workspaces_from_file()
        if not workspaces:
            raise BitbucketException("No workspaces found.")
        print("Select a workspace:")
        workspace = selectOne(workspaces)
        return workspace

    def new_repo(self):
        repo_name = input("Enter the new repository name: ")
        if not repo_name:
            raise BitbucketException("Repository name cannot be empty.")

        workspace = self.select_workspace()
        if not self.check_repo_and_workspace_in_file(repo_name, workspace):
            raise BitbucketException(
                f"Repository '{repo_name}' already exists in workspace '{workspace}'."
            )

        account = self._choose_account_by_email()
        project_key = account.project_key
        bb_api = BitbucketApi(account.username, account.app_password)

        new_repo = bb_api._createRepoOnBitbucketApi(
            workspace=workspace, project_key=project_key, repo_name=repo_name
        )
        if new_repo.status_code in (200, 201):
            print(f"[green]✅ Repository '{repo_name}' created successfully!")
            self.is_in_new_account = True
            return repo_name
        else:
            raise BitbucketException(
                f"Failed to create repository '{repo_name}'. "
                f"Status code: {new_repo.status_code}"
            )

    def set_repo_name(self) -> str:
        pretty_print("Please enter the new repository name:")
        repo_name = input("Enter the new repository name: ")
        if not repo_name:
            raise BitbucketException("Repository name cannot be empty.")
        return repo_name
