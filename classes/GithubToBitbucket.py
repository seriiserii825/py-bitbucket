import os
import subprocess

from classes.AccountsCsv import AccountsCsv
from classes.Bitbucket import Bitbucket
from classes.BitbucketApi import BitbucketApi
from execeptions.BitbucketException import BitbucketException
from pyfzf.pyfzf import FzfPrompt
from utils import pretty_print

fzf = FzfPrompt()


class GithubToBitbucket:
    def __init__(self):
        self.start()

    def start(self):
        print("Starting migration from GitHub to Bitbucket...")
        self._from_github_to_bitbucket()

    def _from_github_to_bitbucket(self):
        repo_name = self._clone_mirror_from_github()
        self._cd_cloned_repo(repo_name)
        bb = Bitbucket()
        workspace = bb.select_workspace()
        workspace = workspace.strip()
        self._create_repo_on_bitbucket(repo_name, workspace)
        self._push_mirror_to_bitbucket(repo_name, workspace)

    def _clone_mirror_from_github(self) -> str:
        github_repos = self._get_github_repos_from_file()
        selected = fzf.prompt(github_repos)
        repo_name = selected[0]
        username = self._get_github_username()
        clone_url = f"git@github.com:{username}/{repo_name}.git"
        command = f"git clone --mirror {clone_url}"
        print(f"command: {command}")
        os.system(command)
        return repo_name

    def _cd_cloned_repo(self, repo_name: str):
        repo_git_name = f"{repo_name}.git"
        if not os.path.exists(repo_git_name):
            print(f"Repository {repo_git_name} does not exist.")
            exit(1)
        os.chdir(repo_git_name)

    def _create_repo_on_bitbucket(self, repo_name: str, workspace: str):
        ac = AccountsCsv()
        account = ac.choose_account_by_email()
        bb_api = BitbucketApi(account.username, account.app_password)
        response = bb_api._createRepoOnBitbucketApi(
            workspace=workspace,
            project_key=account.project_key,
            repo_name=repo_name,
        )
        if response.status_code in (200, 201):
            print(f"✅ Repository '{repo_name}' created on Bitbucket workspace '{workspace}'.")
        else:
            raise BitbucketException(
                f"Failed to create repository '{repo_name}' on Bitbucket. "
                f"Status code: {response.status_code} - {response.text}"
            )

    def _push_mirror_to_bitbucket(self, repo_name: str, workspace: str):
        pretty_print("Pushing mirror to Bitbucket...")
        bb = Bitbucket()
        try:
            bb.push_to_mirror_repo(repo_name, workspace)
            print(f"✅ Repository '{repo_name}' pushed to Bitbucket workspace '{workspace}'.")
        except BitbucketException as e:
            raise BitbucketException(f"Failed to push mirror to Bitbucket: {e}")

    def _get_github_repos_from_file(self) -> list:
        import csv
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(root_dir, "github_repos.csv")
        repos = []
        with open(file_path, mode="r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                repos.append(row[0])
        if not repos:
            raise BitbucketException("No GitHub repositories found in github_repos.csv.")
        return repos

    def _get_github_username(self) -> str:
        import os as _os
        from pathlib import Path
        from dotenv import load_dotenv
        root_dir = Path(__file__).resolve().parents[1]
        load_dotenv(root_dir / ".env")
        username = _os.getenv("GITHUB_USERNAME")
        if not username:
            raise BitbucketException("GITHUB_USERNAME not found in .env file.")
        return username
