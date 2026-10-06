import csv
import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from pyfzf.pyfzf import FzfPrompt
from rich import print

from execeptions.ForgejoException import ForgejoException
from utils import pretty_print, selectMultiple

fzf = FzfPrompt()


class ForgejoClass:
    def __init__(self):
        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(self.ROOT_DIR, "forgejo_repos.csv")

    def _get_data_from_env(self, key: str) -> str:
        dotenv_path = Path(__file__).resolve().parents[1] / ".env"
        load_dotenv(dotenv_path)
        value = os.getenv(key)
        if not value:
            raise ForgejoException(f"{key} not found or empty in .env file.")
        return value

    def _base_url(self) -> str:
        return self._get_data_from_env("FORGEJO_URL").rstrip("/")

    def username(self) -> str:
        return self._get_data_from_env("FORGEJO_USERNAME")

    def _api(self, method: str, path: str, **kwargs) -> requests.Response:
        token = self._get_data_from_env("FORGEJO_TOKEN")
        headers = {"Authorization": f"token {token}", "Accept": "application/json"}
        url = f"{self._base_url()}/api/v1{path}"
        try:
            return requests.request(method, url, headers=headers, timeout=30, **kwargs)
        except requests.RequestException as e:
            raise ForgejoException(f"Request to {url} failed: {e}")

    @staticmethod
    def _error_message(response: requests.Response) -> str:
        try:
            return response.json().get("message", "Unknown error")
        except ValueError:
            return response.text or "Unknown error"

    def ssh_url(self, repo_name: str) -> str:
        host = urlparse(self._base_url()).hostname
        return f"git@{host}:{self.username()}/{repo_name}.git"

    def export_repos_to_csv(self):
        pretty_print("Fetching repositories from Forgejo...")
        names = []
        page = 1
        while True:
            response = self._api("GET", "/user/repos", params={"page": page, "limit": 50})
            if response.status_code != 200:
                raise ForgejoException(
                    f"Failed to list repositories: {response.status_code} "
                    f"- {self._error_message(response)}"
                )
            batch = response.json()
            if not batch:
                break
            names.extend(repo["name"] for repo in batch)
            page += 1

        with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name"])
            for name in names:
                writer.writerow([name])
        pretty_print(f"Saved {len(names)} repositories to {self.file_path}")

    def _get_repos_from_file(self):
        if not os.path.exists(self.file_path):
            raise ForgejoException("forgejo_repos.csv not found. Run 'Forgejo repos to CSV' first.")
        with open(self.file_path, mode="r") as file:
            reader = csv.reader(file)
            next(reader)
            repos = [row[0] for row in reader if row]
        if not repos:
            raise ForgejoException("No repositories found in the file.")
        return repos

    def _get_repo_from_file(self) -> str:
        selected = fzf.prompt(self._get_repos_from_file())
        if not selected:
            raise ForgejoException("No repository selected.")
        return selected[0]

    def repo_exists(self, repo_name: str) -> bool:
        response = self._api("GET", f"/repos/{self.username()}/{repo_name}")
        return response.status_code == 200

    def create_repo_from_folder(self):
        folder_name = os.path.basename(os.getcwd())
        agree = (
            input(f"From current folder name, '{folder_name}', are you agree, (y/n): ")
            .strip()
            .lower()
        )
        if agree != "y":
            raise ForgejoException("Exiting without creating repository.")
        self._create_repo(folder_name)
        self._push_created_repo(folder_name)

    def create_repo_by_arg(self, repo_name: str):
        self._create_repo(repo_name)

    def _create_repo(self, repo_name: str):
        is_private = input("Make repository private? (y/n): ").strip().lower() == "y"
        repo_data = {
            "name": repo_name,
            "description": "Created via Python script",
            "private": is_private,
        }
        response = self._api("POST", "/user/repos", json=repo_data)
        if response.status_code == 201:
            print(f"✅ Repository '{repo_name}' created successfully.")
            print(f"🔗 URL: {response.json().get('html_url')}")
        else:
            raise ForgejoException(
                f"Error creating repository: {response.status_code} "
                f"- {self._error_message(response)}"
            )

    def _push_created_repo(self, repo_name: str):
        try:
            repo_url = self.ssh_url(repo_name)
            os.system("touch README.md")
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
            subprocess.run(["git", "branch", "-M", "main"], check=True)
            subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            print("🚀 Code pushed to Forgejo!")
        except subprocess.CalledProcessError as e:
            print("❌ Git command failed:", e)

    def clone_repo(self):
        repo_name = self._get_repo_from_file()
        clone_url = self.ssh_url(repo_name)
        try:
            subprocess.run(["git", "clone", clone_url], check=True)
            pretty_print(f"🔗 URL: {clone_url}")
        except subprocess.CalledProcessError as e:
            raise ForgejoException(f"Failed to clone repository: {e}")

    def delete_repos(self):
        pretty_print("Deleting multiple repositories on Forgejo...")
        selected_repos = selectMultiple(self._get_repos_from_file())
        if not selected_repos:
            raise ForgejoException("No repositories selected for deletion.")
        pretty_print(f"Selected repositories for deletion: {selected_repos}")
        for repo_name in selected_repos:
            self.delete_repo(repo_name)

    def delete_repo(self, repo_name_arg: str = ""):
        repo_name = repo_name_arg or self._get_repo_from_file()
        response = self._api("DELETE", f"/repos/{self.username()}/{repo_name}")
        if response.status_code == 204:
            print(f"✅ Repository '{repo_name}' deleted successfully.")
        elif response.status_code == 404:
            raise ForgejoException(f"Repository '{repo_name}' not found or insufficient permissions.")
        else:
            raise ForgejoException(
                f"Failed to delete repository '{repo_name}': {response.status_code} "
                f"- {self._error_message(response)}"
            )

    def rename_repo_from_cwd(self):
        pretty_print("Renaming repository from current folder...")
        username = self.username()

        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                check=True, capture_output=True, text=True
            )
        except subprocess.CalledProcessError:
            raise ForgejoException("No git remote 'origin' found in current directory.")

        remote_url = result.stdout.strip()
        repo_name = remote_url.rstrip("/").split("/")[-1].removesuffix(".git")

        current_dir = os.getcwd()
        folder_name = os.path.basename(current_dir)
        if folder_name != repo_name:
            raise ForgejoException(
                f"Current folder name '{folder_name}' does not match "
                f"the Forgejo repository name '{repo_name}'. "
                "Make sure you are running this from the correct repo folder."
            )
        pretty_print(f"Current repo: {repo_name}")

        new_name = input(f"Enter new name for '{repo_name}': ").strip()
        if not new_name:
            raise ForgejoException("New repository name cannot be empty.")

        response = self._api("PATCH", f"/repos/{username}/{repo_name}", json={"name": new_name})
        if response.status_code == 200:
            print(f"✅ Repository '{repo_name}' renamed to '{new_name}' successfully.")
        elif response.status_code == 404:
            raise ForgejoException("Repository not found or insufficient permissions.")
        else:
            raise ForgejoException(
                f"Failed to rename repository: {response.status_code} "
                f"- {self._error_message(response)}"
            )

        if remote_url.startswith("git@"):
            new_remote_url = self.ssh_url(new_name)
        else:
            new_remote_url = f"{self._base_url()}/{username}/{new_name}.git"
        subprocess.run(["git", "remote", "set-url", "origin", new_remote_url], check=True)
        print(f"🔗 Remote updated to: {new_remote_url}")

        # rename the local folder to match the new repo name and leave it,
        # since the folder we were in no longer exists under its old name
        parent_dir = os.path.dirname(current_dir)
        new_dir = os.path.join(parent_dir, new_name)
        os.chdir(parent_dir)
        os.rename(current_dir, new_dir)
        print(f"📁 Local folder renamed to: {new_dir}")

    def push_mirror(self, repo_name: str):
        repo_url = self.ssh_url(repo_name)
        try:
            subprocess.run(["git", "push", "--mirror", repo_url], check=True)
            print(f"✅ Successfully pushed mirror to Forgejo: {repo_name}")
        except subprocess.CalledProcessError as e:
            raise ForgejoException(f"Failed to push mirror to Forgejo: {e}")
