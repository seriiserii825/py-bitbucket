import requests
import json
import os
from rich import console, print
from requests.auth import HTTPBasicAuth
from modules.getRepoData import getRepoData
from pyfzf.pyfzf import FzfPrompt

fzf = FzfPrompt()

class Bitbucket():
    def __init__(self):
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_DIR = os.path.dirname(self.ROOT_DIR)  # Go one level up to the root directory
        # self.checkConfig()
        self.repo_name = ""
        self.workspace = ""
        self.project_key = ""
        self.username = ""
        self.app_password =""
        self.is_private = True
        self.account = 1
        self.initData("bludelego@gmail.com")
        self.auth = HTTPBasicAuth(self.username, self.app_password)

    def prettyPrint(self,value, error=False):
        if error:
            print("[red]===============================")
            print(value)
            print("[red]===============================")
        else:
            print("[blue]===============================")
            print(value)
            print("[blue]===============================")


    def initData(self, email):
        data = getRepoData(email, self.ROOT_DIR)
        self.workspace = data["workspace"]
        self.project_key = data["project_key"]
        self.username = data["username"]
        self.app_password = data["app_password"]
        self.is_private = data["is_private"]

        if not data:
            self.prettyPrint(f"no data found for email {email}")
            exit()

    # def checkRemoteRepo(self):
    #     url = f"https://api.bitbucket.org/2.0/repositories/{self.old_workspace}/{self.repo_name}"
    #     response = requests.get(url, auth=self.auth)
    #     if response.status_code == 200:
    #         print(f"[green]✅ Repository '{self.repo_name}' exists on the old account.")
    #         self.is_in_old_account = True
    #         return True
    #     elif response.status_code == 404:
    #         print(f"[red]❌ Repository '{self.repo_name}' does not exist on the old account.")
    #         return False
    #     else:
    #         print(f"[red]❌ Failed to check repository. Status code: {response.status_code}")
    #         print(response.json())
    #         return False
    #
    # def checkRepoOnNewAccount(self):
    #     print(f'self.repo_name: {self.repo_name}')
    #     url = f"https://api.bitbucket.org/2.0/repositories/{self.new_workspace}/{self.repo_name}"
    #     response = requests.get(url, auth=HTTPBasicAuth(self.new_username, self.new_app_password))
    #     if response.status_code == 200:
    #         print(f"[green]✅ Repository '{self.repo_name}' exists on the new account.")
    #         self.is_in_new_account = True
    #         return True
    #     elif response.status_code == 404:
    #         print(f"[red]❌ Repository '{self.repo_name}' does not exist on the new account.")
    #         return False
    #     else:
    #         print(f"[red]❌ Failed to check repository. Status code: {response.status_code}")
    #         print(response.json())
    #         return False
    #
    # def checkConfig(self):
    #     if not os.path.exists(f"{self.ROOT_DIR}/newRepoData.py") or not os.path.exists(f"{self.ROOT_DIR}/oldRepoData.py"):
    #         print("Please ensure that newRepoData.py and oldRepoData.py are present in the same directory as this script.")
    #         exit()
    #
    # def setRepoName(self):
    #     self.repo_name = input("Enter the repository slug: ")
    #
    # def createRepo(self):
    #     url = f"https://api.bitbucket.org/2.0/repositories/{self.new_workspace}/{self.repo_name}"
    #     payload = {
    #         "scm": "git",
    #         "is_private": self.new_is_private,
    #         "project": {"key": self.new_project_key},
    #         "name": self.repo_name
    #     }
    #     return requests.post(url, json=payload, auth=HTTPBasicAuth(self.new_username, self.new_app_password))
    #
    # def newRepo(self):
    #     if self.is_in_new_account:
    #         print("[green]✅ Repository already exists on the new account. No need to create a new one.")
    #         return
    #
    #     new_repo = self.createRepo()
    #     if new_repo.status_code in (200, 201):
    #         print(f"[green]✅ Repository '{self.repo_name}' created successfully!")
    #         self.is_in_new_account = True
    #         self.openPermissionsInBrowser()
    #     else:
    #         print(f"[red]❌ Failed to create repository. Status code: {new_repo.status_code}")
    #         print(new_repo.json())
    #
    # def checkForNewRepo(self):
    #     repo_url = f"https://api.bitbucket.org/2.0/repositories/{self.new_workspace}/{self.repo_name}"
    #     response = requests.get(repo_url, auth=HTTPBasicAuth(self.new_username, self.new_app_password))
    #     if response.status_code == 200:
    #         print(f"[green]✅ Repository '{self.repo_name}' exists on the new account.")
    #         self.is_in_new_account = True
    #         return True
    #     elif response.status_code == 404:
    #         print(f"[red]❌ Repository '{self.repo_name}' does not exist on the new account.")
    #         return False
    #     else:
    #         print(f"[red]❌ Failed to check repository. Status code: {response.status_code}")
    #         print(response.json())
    #         return False
    #
    # def copyOldRepoToNew(self):
    #     if not self.is_in_old_account:
    #         print("[red]❌ Repository does not exist on the old account. Cannot create new repository.")
    #         return
    #
    #     response = self.createRepo()
    #     if response.status_code in (200, 201):
    #         print(f"✅ Repository '{self.repo_name}' created successfully!")
    #         self.is_in_new_account = True
    #         self.cloneOldRepo()
    #         self.openPermissionsInBrowser()
    #         self.pushNewRepo()
    #         self.deleteRepo()
    #     else:
    #         print(f"❌ Failed to create repository. Status code: {response.status_code}")
    #         print(response.json())
    #
    # def openPermissionsInBrowser(self):
    #     if not self.is_in_new_account:
    #         print("[red]❌ Repository does not exist on the new account. Cannot open permissions in browser.")
    #         return
    #     url = f"https://bitbucket.org/{self.new_workspace}/{self.repo_name}/admin/access"
    #     print(f"Opening permissions page for {self.repo_name} in browser...")
    #     os.system(f"google-chrome-stable {url}")
    #
    # def cloneOldRepo(self):
    #     if not self.is_in_old_account:
    #         print("[red]❌ Repository does not exist on the old account. Cannot clone repository.")
    #         return
    #     repo_url = f"git clone --mirror git@bitbucket.org:sites-bludelego/{self.repo_name}.git";
    #     # go to downloads
    #     os.chdir(os.path.expanduser("~/Downloads"))
    #     # clone the old repo
    #     os.system(repo_url)
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
    # def deleteRepo(self):
    #     url = f"https://api.bitbucket.org/2.0/repositories/{self.old_workspace}/{self.repo_name}"
    #     try:
    #         response = requests.delete(url, auth=HTTPBasicAuth(self.old_username, self.old_app_password))
    #         if response.status_code == 204:
    #             print(f"✅ Repository '{self.repo_name}' deleted successfully!")
    #     except requests.exceptions.RequestException as e:
    #         print(f"[red]❌ An error occurred while trying to delete the repository: {e}")
    #
    # def listRepos(self):
    #     self.new_workspace = "blueline2025"
    #     url = f"https://api.bitbucket.org/2.0/repositories/{self.new_workspace}"
    #     try:
    #         repos = []
    #         while url:
    #             response = requests.get(url, auth=HTTPBasicAuth(self.new_username, self.new_username))
    #             if response.status_code == 200:
    #                 data = response.json()
    #                 for repo in data.get("values", []):
    #                     repos.append(repo["name"])
    #                 url = data.get("next")  # Pagination support
    #             else:
    #                 print(f"[red]❌ Failed to fetch repositories: {response.status_code} {response.text}")
    #                 break
    #         print(f"✅ Found {len(repos)} repositories:")
    #         for repo_name in repos:
    #             print(f" - {repo_name}")
    #         return repos
    #     except requests.exceptions.RequestException as e:
    #         print(f"[red]❌ An error occurred while trying to list repositories: {e}")
    #         return []
    #
    def fetchWorkspaceRepos(self, workspaces: list, account: int = 1):
        self.account = account
        self.workspaces = workspaces  # make this a list in case of future expansion
        print("📦 Starting to fetch all repository data...")

        for workspace in self.workspaces:
            count = 1
            while True:
                url = (
                    f"https://api.bitbucket.org/2.0/repositories/{workspace}"
                    f"?pagelen=100&page={count}&fields=next,values.links.branches.href,values.full_name"
                )
                response = requests.get(url, auth=self.auth)
                if response.status_code != 200:
                    print(f"[red]❌ Failed to fetch data: {response.status_code} {response.text}")
                    break

                data = response.json()
                values = data.get("values", [])

                print(f"🔍 Page {count} - Fetched {len(values)} repositories")

                if not values:
                    print("✅ No more repositories found.")
                    break  # Do not return, just break the pagination loop

                # Save raw response to file (optional)
                with open(f"data_page_{count}.json", "w") as f:
                    f.write(response.text)

                # Print names for clarity
                for repo in values:
                    print(f"📁 {repo['full_name']}")

                count += 1

        print("🎉 All repositories fetched.")
        os.system('rm data_page*.json')

    def chooseWorkspaces(self):
        url = "https://api.bitbucket.org/2.0/workspaces"
        response = requests.get(url, auth=self.auth)
        workspaces = []
        if response.ok:
            data = response.json()
            for item in data.get("values", []):
                workspace = item['slug'] 
                workspaces.append(workspace)
            workspace = fzf.prompt(workspaces)
            self.workspace = workspace[0]
            self.prettyPrint(f"Selected workspace: {self.workspace}")
        else:
            self.prettyPrint(response.text, error=True)
            print(response.text)
            exit()
    #
    # def list_projects(self, workspace, old=False):
    #     if old:
    #         print("\033[92mListing old projects...\033[0m")  # green text
    #         username = self.old_username
    #         app_password = self.old_app_password
    #     else:
    #         username = self.new_username
    #         app_password = self.new_app_password
    #     print(f"\033[92mListing projects in workspace '{workspace}'...\033[0m")  # green text
    #     url = f"https://api.bitbucket.org/2.0/workspaces/{workspace}/projects"
    #     response = requests.get(url, auth=HTTPBasicAuth(username, app_password))
    #     print(f"HTTP STATUS: {response.status_code}")
    #     if response.ok:
    #         data = response.json()
    #         print(json.dumps(data, indent=2))
    #     else:
    #         print("Failed to list projects.")
    #         print(response.text)

