from classes.GithubClass import GithubClass
from execeptions.GithubException import GithubException
from utils import pretty_print


class BitbucketToGithub:
    def __init__(self):
        self.start()

    def start(self):
        print("Starting migration from Bitbucket to GitHub...")
        self._from_bitbucket_to_github()

    def _from_bitbucket_to_github(self):
        gth = GithubClass()
        try:
            repo_name = gth.clone_mirror_from_bitbucket()
            repo_exists_on_github = gth.check_repo_on_github(repo_name)
            if repo_exists_on_github:
                raise GithubException(
                    f"Repository {repo_name} already exists on GitHub."
                )
            gth.create_repo_by_arg(repo_name)
            gth.push_mirror_to_github(repo_name)
        except GithubException as e:
            pretty_print(f"Error: {e}", error=True)
