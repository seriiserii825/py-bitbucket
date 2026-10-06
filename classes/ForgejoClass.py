import csv
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from pyfzf.pyfzf import FzfPrompt
from rich import print

from execeptions.ForgejoException import ForgejoException
from utils import pretty_print, pretty_table, selectMultiple, selectOne

fzf = FzfPrompt()

# repo units a newly created team gets access to
TEAM_UNITS = [
    "repo.code",
    "repo.issues",
    "repo.ext_issues",
    "repo.wiki",
    "repo.ext_wiki",
    "repo.pulls",
    "repo.releases",
    "repo.projects",
    "repo.packages",
    "repo.actions",
]


class ForgejoClass:
    """
    Repos are identified by their full name "owner/name", because a repo
    can belong either to the user or to the organization.
    """

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

    def _check(self, response: requests.Response, expected: int, action: str):
        if response.status_code == expected:
            return
        try:
            message = response.json().get("message", "Unknown error")
        except ValueError:
            message = response.text or "Unknown error"
        raise ForgejoException(f"Failed to {action}: {response.status_code} - {message}")

    def _get_paginated(self, path: str, action: str) -> list:
        items: list = []
        page = 1
        while True:
            response = self._api("GET", path, params={"page": page, "limit": 50})
            self._check(response, 200, action)
            batch = response.json()
            if not batch:
                return items
            items.extend(batch)
            page += 1

    def ssh_url(self, full_name: str) -> str:
        host = urlparse(self._base_url()).hostname
        return f"git@{host}:{full_name}.git"

    # ---------- organization / teams ----------

    def select_org(self) -> str:
        orgs = [o["username"] for o in self._get_paginated("/user/orgs", "list organizations")]
        if not orgs:
            raise ForgejoException("You are not a member of any organization.")
        if len(orgs) == 1:
            return orgs[0]
        return selectOne(orgs)

    def get_teams(self, org: str) -> list:
        return self._get_paginated(f"/orgs/{org}/teams", "list teams")

    def list_teams(self):
        org = self.select_org()
        teams = self.get_teams(org)
        rows = []
        for t in teams:
            repos = self._get_paginated(f"/teams/{t['id']}/repos", f"list repos of team {t['name']}")
            repos_text = "all" if t.get("includes_all_repositories") else str(len(repos))
            rows.append([t["name"], t.get("permission", ""), repos_text, t.get("description", "")])
        pretty_table(f"Teams in {org}", ["Name", "Permission", "Repos", "Description"], rows)

    def list_team_repos(self):
        org = self.select_org()
        teams = self.get_teams(org)
        if not teams:
            raise ForgejoException(f"No teams found in '{org}'.")
        names = [t["name"] for t in teams]
        team = teams[names.index(selectOne(names))]
        if team.get("includes_all_repositories"):
            repos = self._get_paginated(f"/orgs/{org}/repos", "list organization repositories")
        else:
            repos = self._get_paginated(f"/teams/{team['id']}/repos", f"list repos of team {team['name']}")
        rows = [
            [r["full_name"], "private" if r.get("private") else "public", r.get("ssh_url", "")]
            for r in sorted(repos, key=lambda r: r["full_name"])
        ]
        pretty_table(f"Repos of team '{team['name']}' ({len(rows)})", ["Repo", "Visibility", "SSH"], rows)

    def create_team(self):
        org = self.select_org()
        name = input("Team name: ").strip()
        if not name:
            raise ForgejoException("Team name cannot be empty.")
        description = input("Description (optional): ").strip()
        print("[yellow]Permission for team members on the team's repos:")
        permission = selectOne(["write", "read", "admin"])
        data = {
            "name": name,
            "description": description,
            "permission": permission,
            "units": TEAM_UNITS,
            "includes_all_repositories": False,
            "can_create_org_repo": False,
        }
        response = self._api("POST", f"/orgs/{org}/teams", json=data)
        self._check(response, 201, f"create team '{name}'")
        print(f"✅ Team '{name}' ({permission}) created in '{org}'.")
        print(f"🔗 Add members: {self._base_url()}/org/{org}/teams/{name.lower()}")

    def _choose_owner(self) -> tuple[str, dict | None]:
        """
        Returns (owner, team): either the user's own account (team None)
        or the organization plus the team the repo should be added to.
        """
        username = self.username()
        org = self.select_org()
        teams = self.get_teams(org)
        personal = f"Personal ({username})"
        options = [f"{org} / team: {t['name']}" for t in teams] + [personal]
        print("[yellow]Where to create the repository?")
        choice = selectOne(options)
        if choice == personal:
            return username, None
        return org, teams[options.index(choice)]

    # ---------- repos ----------

    def export_repos_to_csv(self):
        pretty_print("Fetching repositories from Forgejo...")
        repos = self._get_paginated("/user/repos", "list repositories")
        for org in self._get_paginated("/user/orgs", "list organizations"):
            repos += self._get_paginated(f"/orgs/{org['username']}/repos", "list organization repositories")
        names = sorted({repo["full_name"] for repo in repos})

        with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["FullName"])
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
        if any("/" not in r for r in repos):
            raise ForgejoException("forgejo_repos.csv is outdated. Run 'Forgejo repos to CSV' again.")
        return repos

    def _get_repo_from_file(self) -> str:
        selected = fzf.prompt(self._get_repos_from_file())
        if not selected:
            raise ForgejoException("No repository selected.")
        return selected[0]

    def find_repo(self):
        full_name = self._get_repo_from_file()
        response = self._api("GET", f"/repos/{full_name}")
        self._check(response, 200, f"get repository '{full_name}'")
        repo = response.json()

        teams_text = "-"
        if repo.get("owner", {}).get("username") != self.username():
            response = self._api("GET", f"/repos/{full_name}/teams")
            self._check(response, 200, f"list teams of '{full_name}'")
            teams = [f"{t['name']} ({t.get('permission', '')})" for t in response.json()]
            teams_text = ", ".join(teams) or "-"

        rows = [
            ["Repo", repo["full_name"]],
            ["Teams", teams_text],
            ["Visibility", "private" if repo.get("private") else "public"],
            ["Default branch", repo.get("default_branch", "")],
            ["Description", repo.get("description", "")],
            ["Updated", repo.get("updated_at", "")],
            ["Web", repo.get("html_url", "")],
            ["SSH", repo.get("ssh_url", "")],
        ]
        pretty_table(f"Repo {full_name}", ["Field", "Value"], rows)

    def create_repo_from_folder(self):
        folder_name = os.path.basename(os.getcwd())
        agree = (
            input(f"From current folder name, '{folder_name}', are you agree, (y/n): ")
            .strip()
            .lower()
        )
        if agree != "y":
            raise ForgejoException("Exiting without creating repository.")
        full_name = self.create_repo_by_arg(folder_name)
        self._push_created_repo(full_name)

    def create_repo_by_arg(self, repo_name: str) -> str:
        """Creates the repo (asks owner/team and visibility), returns its full name."""
        owner, team = self._choose_owner()
        is_private = input("Make repository private? (y/n): ").strip().lower() == "y"
        repo_data = {
            "name": repo_name,
            "description": "Created via Python script",
            "private": is_private,
        }
        path = "/user/repos" if team is None else f"/orgs/{owner}/repos"
        response = self._api("POST", path, json=repo_data)
        self._check(response, 201, f"create repository '{repo_name}'")
        full_name = response.json()["full_name"]
        print(f"✅ Repository '{full_name}' created successfully.")
        print(f"🔗 URL: {response.json().get('html_url')}")

        if team is not None:
            if team.get("includes_all_repositories"):
                print(f"Team '{team['name']}' already has access to all repositories.")
            else:
                response = self._api("PUT", f"/teams/{team['id']}/repos/{full_name}")
                self._check(response, 204, f"add '{full_name}' to team '{team['name']}'")
                print(f"👥 Added to team '{team['name']}'.")
        return full_name

    def _push_created_repo(self, full_name: str):
        try:
            repo_url = self.ssh_url(full_name)
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
        clone_url = self.ssh_url(self._get_repo_from_file())
        try:
            subprocess.run(["git", "clone", clone_url], check=True)
            pretty_print(f"🔗 URL: {clone_url}")
        except subprocess.CalledProcessError as e:
            raise ForgejoException(f"Failed to clone repository: {e}")

    def delete_repos(self):
        selected_repos = selectMultiple(self._get_repos_from_file())
        if not selected_repos:
            raise ForgejoException("No repositories selected for deletion.")
        pretty_print(f"Selected repositories for deletion: {selected_repos}")
        for full_name in selected_repos:
            self.delete_repo(full_name)

    def delete_repo(self, full_name_arg: str = ""):
        full_name = full_name_arg or self._get_repo_from_file()
        response = self._api("DELETE", f"/repos/{full_name}")
        self._check(response, 204, f"delete repository '{full_name}'")
        print(f"✅ Repository '{full_name}' deleted successfully.")

    def rename_repo_from_cwd(self):
        pretty_print("Renaming repository from current folder...")
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                check=True, capture_output=True, text=True
            )
        except subprocess.CalledProcessError:
            raise ForgejoException("No git remote 'origin' found in current directory.")

        remote_url = result.stdout.strip()
        # git@host:owner/repo.git or https://host/owner/repo.git
        parts = re.split(r"[:/]", remote_url.rstrip("/"))
        owner, repo_name = parts[-2], parts[-1].removesuffix(".git")

        current_dir = os.getcwd()
        folder_name = os.path.basename(current_dir)
        if folder_name != repo_name:
            raise ForgejoException(
                f"Current folder name '{folder_name}' does not match "
                f"the Forgejo repository name '{repo_name}'. "
                "Make sure you are running this from the correct repo folder."
            )
        pretty_print(f"Current repo: {owner}/{repo_name}")

        new_name = input(f"Enter new name for '{repo_name}': ").strip()
        if not new_name:
            raise ForgejoException("New repository name cannot be empty.")

        response = self._api("PATCH", f"/repos/{owner}/{repo_name}", json={"name": new_name})
        self._check(response, 200, "rename repository")
        print(f"✅ Repository '{repo_name}' renamed to '{new_name}' successfully.")

        if remote_url.startswith("git@"):
            new_remote_url = self.ssh_url(f"{owner}/{new_name}")
        else:
            new_remote_url = f"{self._base_url()}/{owner}/{new_name}.git"
        subprocess.run(["git", "remote", "set-url", "origin", new_remote_url], check=True)
        print(f"🔗 Remote updated to: {new_remote_url}")

        # rename the local folder to match the new repo name and leave it,
        # since the folder we were in no longer exists under its old name
        parent_dir = os.path.dirname(current_dir)
        new_dir = os.path.join(parent_dir, new_name)
        os.chdir(parent_dir)
        os.rename(current_dir, new_dir)
        print(f"📁 Local folder renamed to: {new_dir}")

    def push_mirror(self, full_name: str):
        repo_url = self.ssh_url(full_name)
        try:
            subprocess.run(["git", "push", "--mirror", repo_url], check=True)
            print(f"✅ Successfully pushed mirror to Forgejo: {full_name}")
        except subprocess.CalledProcessError as e:
            raise ForgejoException(f"Failed to push mirror to Forgejo: {e}")
