import os
import requests
import subprocess
from dotenv import load_dotenv
from pathlib import Path

from execeptions.GithubException import GithubException


class Github:
    def __init__(self):
        self.repo_http = "https://github.com/seriiserii825"
        self.repo_name = ""

    def setRepoName(self):
        self.repo_name = input("Enter the repository name: ")

    def findRepo(self):
        username = "seriiserii825"  # default username
        word_in_repo = input("Enter a word to search in your repositories: ")
        url = "https://api.github.com/search/repositories"
        params = {
            "q": f"{word_in_repo} user:{username} in:name",
            "sort": "stars",
            "order": "desc",
            "per_page": 10
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            total = data.get("total_count", 0)
            if total > 0:
                print(
                    f"✅ Found {total} repositories in user '{username}' containing '{word_in_repo}':")
                for repo in data["items"]:
                    print(f"- {repo['full_name']}: {repo['html_url']}")
            else:
                print(
                    f"❌ No repositories found in user '{username}' containing '{word_in_repo}'.")
        else:
            print(
                f"❌ Failed to search repositories. Status code: {response.status_code}")

    def checkRepo(self):
        url = f"{self.repo_http}/{self.repo_name}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"[green]✅ Repository '{self.repo_name}' exists on GitHub.")
            return True
        elif response.status_code == 404:
            print(
                f"[red]❌ Repository '{self.repo_name}' does not exist on GitHub.")
            return False
        else:
            print(
                f"[red]❌ Failed to check repository. Status code: {response.status_code}")
            return False

    def clone_repo(self):
        repo_name = input("Enter the repository name to clone: ")
        if not repo_name:
            print("[red]❌ Repository name cannot be empty.")
            return
        if not self.checkRepo():
            print("[red]❌ Cannot clone repository that does not exist.")
            return
        clone_url = f"git@github.com:seriiserii825/{repo_name}.git"

        try:
            subprocess.run(["git", "clone", clone_url], check=True)
            print(
                f"[green]✅ Repository '{self.repo_name}' cloned successfully!")
        except subprocess.CalledProcessError as e:
            print(f"[red]❌ Failed to clone repository: {e}")

    def create_repo(self):
        folder_name = os.path.basename(os.getcwd())
        agree = input(
            f"From current folder name, '{folder_name}', are you agree, (y/n): ").strip().lower()
        if agree != 'y':
            exit("Exiting without creating repository.")

        USERNAME = self._get_data_from_env("GITHUB_USERNAME")
        TOKEN = self._get_data_from_env("GITHUB_TOKEN")

        repo_data = {
            "name": folder_name,
            "description": "Created via Python script",
            "private": False  # Set to True for a private repository
        }

        url = "https://api.github.com/user/repos"

        response = requests.post(
            url,
            json=repo_data,
            auth=(USERNAME, TOKEN)
        )

        if response.status_code == 201:
            print(f"✅ Repository '{repo_data['name']}' created successfully.")
            print(f"🔗 URL: {response.json()['html_url']}")
        else:
            print(f"❌ Failed to create repository: {response.status_code}")
            raise GithubException(
                f"Error creating repository: \
                {response.json().get('message', 'Unknown error')}")
        try:
            repo_url = f"git@github.com:seriiserii825/{folder_name}.git"
            os.system("touch README.md")
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"], check=True)
            subprocess.run(["git", "branch", "-M", "main"], check=True)
            subprocess.run(
                ["git", "remote", "add", "origin", repo_url], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            print("🚀 Code pushed to GitHub!")
        except subprocess.CalledProcessError as e:
            print("❌ Git command failed:", e)

    def delete_repo(self):
        token = self._get_data_from_env("GITHUB_TOKEN")
        username = self._get_data_from_env("GITHUB_USERNAME")
        repo_name = input("Enter the repository name to delete: ")
        if not repo_name:
            print("❌ Repository name cannot be empty.")
            return
        url = f"https://api.github.com/repos/{username}/{repo_name}"
        headers = {
            "Accept": "application/vnd.github.v3+json",
        }

        response = requests.delete(url, auth=(
            username, token), headers=headers)

        if response.status_code == 204:
            print(f"✅ Repository '{repo_name}' deleted successfully.")
        elif response.status_code == 404:
            raise GithubException(
                "Repository not found or insufficient permissions.")
        else:
            raise GithubException(
                f"Failed to delete repository: {response.status_code} - {response.json().get('message', 'Unknown error')}")

    def _get_data_from_env(self, key: str) -> str:
        current_script_path = Path(__file__).resolve()
        dotenv_path = current_script_path.parents[1] / '.env'
        load_dotenv(dotenv_path)

        if not os.getenv(key):
            raise GithubException(
                f"{key} not found in .env file.")
        api_key = os.getenv(key)
        if not api_key:
            raise GithubException(f"{key} is empty in .env file.")
        return api_key
