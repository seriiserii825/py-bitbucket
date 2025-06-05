import requests
import subprocess

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
        
        clone_url = f"{self.repo_http}/{self.repo_name}.git"
        try:
            subprocess.run(["git", "clone", clone_url], check=True)
            print(f"[green]✅ Repository '{self.repo_name}' cloned successfully!")
        except subprocess.CalledProcessError as e:
            print(f"[red]❌ Failed to clone repository: {e}")
