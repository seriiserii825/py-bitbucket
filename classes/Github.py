import requests
import subprocess

from githubData import githubData

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
                print(f"✅ Found {total} repositories in user '{username}' containing '{word_in_repo}':")
                for repo in data["items"]:
                    print(f"- {repo['full_name']}: {repo['html_url']}")
            else:
                print(f"❌ No repositories found in user '{username}' containing '{word_in_repo}'.")
        else:
            print(f"❌ Failed to search repositories. Status code: {response.status_code}")

    def checkRepo(self):
        url = f"{self.repo_http}/{self.repo_name}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"[green]✅ Repository '{self.repo_name}' exists on GitHub.")
            return True
        elif response.status_code == 404:
            print(f"[red]❌ Repository '{self.repo_name}' does not exist on GitHub.")
            return False
        else:
            print(f"[red]❌ Failed to check repository. Status code: {response.status_code}")
            return False

    def cloneRepo(self):
        if not self.checkRepo():
            print("[red]❌ Cannot clone repository that does not exist.")
            return
        clone_url = f"git@github.com:seriiserii825/{self.repo_name}.git"

        try:
            subprocess.run(["git", "clone", clone_url], check=True)
            print(f"[green]✅ Repository '{self.repo_name}' cloned successfully!")
        except subprocess.CalledProcessError as e:
            print(f"[red]❌ Failed to clone repository: {e}")

    def createRepo(self):
        """
        Creates a new repository on GitHub and pushes the current code to it.
        Repo name is set by folder name
        """
        folder_name = subprocess.run(["basename", "$PWD"], capture_output=True, text=True, shell=True).stdout.strip()
        print(f"folder_name: {folder_name}")
        agree = input(f"Repo name will be from current folder name, {folder_name}, are you agree, (y/n): ").strip().lower()
        if agree != 'y':
            exit("Exiting without creating repository.")
        data = githubData()
        token = data["token"]
        # get current folder name
        repo_name = folder_name
        username = "seriiserii825"
        description = "Repo created using Python script"
        private = True

        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        payload = {
            "name": repo_name,
            "description": description,
            "private": private
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 201:
            print(f"✅ Repository '{repo_name}' created on GitHub.")
            repo_url = f"https://github.com/{username}/{repo_name}.git"
        else:
            print(f"❌ Failed to create repository: {response.status_code}")
            print(response.json())
            exit(1)

        try:
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
            subprocess.run(["git", "branch", "-M", "main"], check=True)
            subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            print("🚀 Code pushed to GitHub!")
        except subprocess.CalledProcessError as e:
            print("❌ Git command failed:", e)
