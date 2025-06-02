import requests
import json
import os
from requests.auth import HTTPBasicAuth
from newRepoData import newRepoData
from oldRepoData import oldRepoData

if not os.path.exists("newRepoData.py") or not os.path.exists("oldRepoData.py"):
    print("Please ensure that newRepoData.py and oldRepoData.py are present in the same directory as this script.")
    exit()

new_data = newRepoData()
old_data = oldRepoData()

new_workspace = new_data["new_workspace"]
new_project_key = new_data["new_project_key"]
new_username = new_data["new_username"]
new_app_password = new_data["new_app_password"]
new_is_private = new_data["new_is_private"]

old_workspace = old_data["old_workspace"]
old_project_key = old_data["old_project_key"]
old_username = old_data["old_username"]
old_app_password = old_data["old_app_password"]
old_is_private = old_data["old_is_private"]

repo_name = input("Enter the repository slug: ")

def create_repo():
    url = f"https://api.bitbucket.org/2.0/repositories/{new_workspace}/{repo_name}"
    payload = {
        "scm": "git",
        "is_private": new_is_private,
        "project": {"key": new_project_key},
        "name": repo_name
    }
    response = requests.post(url, json=payload, auth=HTTPBasicAuth(new_username, new_app_password))
    if response.status_code in (200, 201):
        print(f"✅ Repository '{repo_name}' created successfully!")
    else:
        print(f"❌ Failed to create repository. Status code: {response.status_code}")
        print(response.json())

def cloneOldRepo():
    repo_url = f"git clone --mirror git@bitbucket.org:sites-bludelego/{repo_name}.git";
    # go to downloads
    os.chdir(os.path.expanduser("~/Downloads"))
    # clone the old repo
    os.system(repo_url)

def push_to_new_repo():
    old_repo_path = os.path.join(os.path.expanduser("~/Downloads"), repo_name + ".git")
    os.chdir(old_repo_path)
    push_command = f"git push --mirror git@bitbucket.org:blueline2025/bs-bmp-modena.git"
    print(f"Executing command: {push_command}")
    os.system(push_command)

def delete_repo():
    url = f"https://api.bitbucket.org/2.0/repositories/{old_workspace}/{repo_name}"
    response = requests.delete(url, auth=HTTPBasicAuth(old_username, old_app_password))
    if response.status_code == 204:
        print(f"✅ Repository '{repo_name}' deleted successfully!")
    else:
        print(f"❌ Failed to delete repository. Status code: {response.status_code}")
        print(response.json())

def list_workspaces(old=False):
    if old:
        print("Listing old workspaces...")  # green text
        username = old_username
        app_password = old_app_password
    else:
        username = new_username
        app_password = new_app_password
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

def list_projects(workspace, old=False):
    if old:
        print("\033[92mListing old projects...\033[0m")  # green text
        username = old_username
        app_password = old_app_password
    else:
        username = new_username
        app_password = new_app_password
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


def openPermissionsInBrowser(workspace, repo_slug):
    url = f"https://bitbucket.org/{workspace}/{repo_slug}/admin/access"
    # open in browser
    print(f"Opening URL: {url}")
    os.system(f"firefox {url}")
    to_push = input("Do you want to push the changes to the new repo? (y/n): ")
    if to_push.lower() == 'y':
        push_to_new_repo()
    else:
        print("Changes not pushed to the new repo.")

if __name__ == "__main__":
    choose = input("Create a new repo, or push to an existing one? (n/e): ").strip().lower()
    if choose == 'n':
        cloneOldRepo()
        create_repo()
        openPermissionsInBrowser(new_workspace, repo_name)
    elif choose == 'e':
        openPermissionsInBrowser(new_workspace, repo_name)
    else:
        print("Invalid choice. Exiting.")
        exit()
