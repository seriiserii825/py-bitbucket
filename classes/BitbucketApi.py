import requests
from requests.auth import HTTPBasicAuth

from execeptions.BitbucketApiException import BitbucketApiException
from my_types.repo_type import RepoType
from utils import pretty_print


class BitbucketApi:
    def __init__(self, username, app_password):
        self.workspace = ''
        self.username = username
        self.app_password = app_password
        self.auth = HTTPBasicAuth(self.username, self.app_password)

    def fetch_workspace_list(self):
        url = "https://api.bitbucket.org/2.0/workspaces"
        response = requests.get(url, auth=self.auth)
        workspaces = []
        if response.ok:
            data = response.json()
            for item in data.get("values", []):
                workspace = item['slug']
                workspaces.append(workspace)
            return workspaces
        else:
            raise BitbucketApiException(
                f"Error fetching workspaces: {response.status_code} {response.text}"
            )

    def fetch_workspace_repos(self, workspace) -> list[RepoType]:
        repos: list[RepoType] = []

        url = (
            f"https://api.bitbucket.org/2.0/repositories/{workspace}"
            f"?pagelen=100&fields=next,values.links.branches.href,values.full_name"
        )
        count = 1
        while url:
            response = requests.get(url, auth=self.auth)
            if response.status_code != 200:
                raise BitbucketApiException(
                    f"Error fetching repositories: "
                    f"{response.status_code} {response.text}",
                )
            data = response.json()
            values = data.get("values", [])
            if not values:
                pretty_print("No more repositories to fetch.", error=True)
                break
            for repo in values:
                repos.append(RepoType(
                    name=repo["full_name"],
                    workspace=workspace,
                ))
            url = data.get("next")  # Get the next page URL
            count += 1
        # Optionally clean up
        return repos
