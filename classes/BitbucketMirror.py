import os
from classes.Bitbucket import Bitbucket
from classes.Browser import Browser
from execeptions.BitbucketException import BitbucketException
from my_types.repo_type import RepoType
from utils import pretty_print


class BitbucketMirror:
    def __init__(self):
        self.start()

    def start(self):
        repo_name, _ = self._clone_mirror_from_bitbucket()
        self._cd_cloned_repo(repo_name)
        workspace = self._select_workspace()
        self._create_and_edit_group_in_browser(workspace, repo_name)
        self._push_to_new_repo(repo_name, workspace)

    def _clone_mirror_from_bitbucket(self) -> RepoType:
        pretty_print("Cloning mirror from Bitbucket...")
        bb = Bitbucket()
        name, workspace = bb.get_repo_from_file()
        bb.clone_repo(name, workspace, mirror=True)
        return RepoType(name=name, workspace=workspace)

    def _cd_cloned_repo(self, repo_name: str):
        repo_git_name = f"{repo_name}.git"
        if not os.path.exists(repo_git_name):
            print(f"Repository {repo_git_name} does not exist.")
            exit(1)
        os.chdir(repo_git_name)

    def _select_workspace(self) -> str:
        pretty_print("Selecting workspace...")
        bb = Bitbucket()
        workspace = bb.select_workspace()
        # trim whitespace from workspace
        workspace = workspace.strip()
        return workspace

    def _create_and_edit_group_in_browser(self, workspace: str, repo_name: str):
        pretty_print(f"Creating new repo in workspace: {workspace}")
        bw = Browser(workspace, repo_name)
        bw.create_repo_in_browser()
        bw.edit_group_in_browser(workspace, repo_name)

    def _push_to_new_repo(self, repo_name: str, workspace: str):
        pretty_print("Pushing to new Bitbucket repository...")
        bb = Bitbucket()
        try:
            bb.push_to_mirror_repo(repo_name, workspace)
            print(f"Repository {repo_name} has been pushed to Bitbucket.")
        except BitbucketException as e:
            print(f"Error pushing to Bitbucket: {e}")
            bw = Browser(workspace, repo_name)
            bw.change_main_barnch_in_browser(repo_name, workspace)
            bb.push_to_mirror_repo(repo_name, workspace)
        bb.set_mirror_origin(repo_name, workspace)
