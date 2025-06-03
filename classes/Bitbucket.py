import requests
import json
import os
from rich import print
from requests.auth import HTTPBasicAuth
from newRepoData import newRepoData
from oldRepoData import oldRepoData

class Bitbucket:
    def __init__(self):
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_DIR = os.path.dirname(self.ROOT_DIR)  # Go one level up to the root directory
        self.checkConfig()
        self.initNewData()
        self.initOldData()
        self.repo_name = ""

    def checkRepoOnOldAccount(self):
        url = f"https://api.bitbucket.org/2.0/repositories/{self.old_workspace}/{self.repo_name}"
        response = requests.get(url, auth=HTTPBasicAuth(self.old_username, self.old_app_password))
        if response.status_code == 200:
            print(f"[green]✅ Repository '{self.repo_name}' exists on the old account.")
            return True
        elif response.status_code == 404:
            print(f"[red]❌ Repository '{self.repo_name}' does not exist on the old account.")
            return False
        else:
            print(f"[red]❌ Failed to check repository. Status code: {response.status_code}")
            print(response.json())
            return False

    def checkConfig(self):
        if not os.path.exists(f"{self.ROOT_DIR}/newRepoData.py") or not os.path.exists(f"{self.ROOT_DIR}/oldRepoData.py"):
            print("Please ensure that newRepoData.py and oldRepoData.py are present in the same directory as this script.")
            exit()

    def initNewData(self):
        new_data = newRepoData()
        self.new_workspace = new_data["new_workspace"]
        self.new_project_key = new_data["new_project_key"]
        self.new_username = new_data["new_username"]
        self.new_app_password = new_data["new_app_password"]
        self.new_is_private = new_data["new_is_private"]

    def initOldData(self):
        old_data = oldRepoData()
        self.old_workspace = old_data["old_workspace"]
        self.old_project_key = old_data["old_project_key"]
        self.old_username = old_data["old_username"]
        self.old_app_password = old_data["old_app_password"]
        self.old_is_private = old_data["old_is_private"]


    def setRepoName(self):
        self.repo_name = input("Enter the repository slug: ")

    def createRepo(self):
        url = f"https://api.bitbucket.org/2.0/repositories/{self.new_workspace}/{self.repo_name}"
        payload = {
            "scm": "git",
            "is_private": self.new_is_private,
            "project": {"key": self.new_project_key},
            "name": self.repo_name
        }
        response = requests.post(url, json=payload, auth=HTTPBasicAuth(self.new_username, self.new_app_password))
        if response.status_code in (200, 201):
            print(f"✅ Repository '{self.repo_name}' created successfully!")
        else:
            print(f"❌ Failed to create repository. Status code: {response.status_code}")
            print(response.json())

    def cloneOldRepo(self):
        repo_url = f"git clone --mirror git@bitbucket.org:sites-bludelego/{self.repo_name}.git";
        # go to downloads
        os.chdir(os.path.expanduser("~/Downloads"))
        # clone the old repo
        os.system(repo_url)

    def pushNewRepo(self):
        old_repo_path = os.path.join(os.path.expanduser("~/Downloads"), self.repo_name + ".git")
        os.chdir(old_repo_path)
        push_command = f"git push --mirror git@bitbucket.org:blueline2025/{self.repo_name}.git"
        print(f"Executing command: {push_command}")
        agree = input("Do you want to push the changes to the new repo? (y/n): ")
        if agree.lower() != 'y':
            print("Push aborted.")
            return
        os.system(push_command)

    def deleteRepo(self):
        url = f"https://api.bitbucket.org/2.0/repositories/{self.old_workspace}/{self.repo_name}"
        try:
            response = requests.delete(url, auth=HTTPBasicAuth(self.old_username, self.old_app_password))
            if response.status_code == 204:
                print(f"✅ Repository '{self.repo_name}' deleted successfully!")
        except requests.exceptions.RequestException as e:
            print(f"[red]❌ An error occurred while trying to delete the repository: {e}")


    def list_workspaces(self, old=False):
        if old:
            print("Listing old workspaces...")  # green text
            username = self.old_username
            app_password = self.old_app_password
        else:
            username = self.new_username
            app_password = self.new_app_password
        print("\033[92mListing workspaces...\033[0m")  # green text
        url = "https://api.bitbucket.org/2.0/workspaces"
        response = requests.get(url, auth=HTTPBasicAuth(username, app_password))
        print(f"HTTP STATUS: {response.status_code}")
        if response.ok:
            data = response.json()
            print(json.dumps(data, indent=2))
        else:
            print("Failed to list workspaces.")
            print(response.text)

    def list_projects(self, workspace, old=False):
        if old:
            print("\033[92mListing old projects...\033[0m")  # green text
            username = self.old_username
            app_password = self.old_app_password
        else:
            username = self.new_username
            app_password = self.new_app_password
        print(f"\033[92mListing projects in workspace '{workspace}'...\033[0m")  # green text
        url = f"https://api.bitbucket.org/2.0/workspaces/{workspace}/projects"
        response = requests.get(url, auth=HTTPBasicAuth(username, app_password))
        print(f"HTTP STATUS: {response.status_code}")
        if response.ok:
            data = response.json()
            print(json.dumps(data, indent=2))
        else:
            print("Failed to list projects.")
            print(response.text)

