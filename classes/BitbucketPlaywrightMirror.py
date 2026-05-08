import os
from classes.Bitbucket import Bitbucket
from classes.BitbucketPlaywright import BitbucketPlaywright
from classes.BitbucketPlaywrightCreateRepo import BitbucketPlaywrightCreateRepo
from execeptions.BitbucketException import BitbucketException
from my_types.repo_type import RepoType
from utils import pretty_print


class BitbucketPlaywrightMirror:
    def __init__(self):
        self.start()

    def start(self):
        repo_name, _ = self._clone_mirror_from_bitbucket()
        self._cd_cloned_repo(repo_name)

        creator = BitbucketPlaywrightCreateRepo(name=repo_name)
        self._push_to_new_repo(repo_name, creator.workspace)

    def _clone_mirror_from_bitbucket(self) -> RepoType:
        pretty_print("Cloning mirror from Bitbucket...")
        bb = Bitbucket()
        name, workspace = bb.get_repo_from_file()
        bb.clone_repo(name, workspace, mirror=True)
        return RepoType(name=name, workspace=workspace)

    def _cd_cloned_repo(self, repo_name: str):
        repo_git_name = f"{repo_name}.git"
        if not os.path.exists(repo_git_name):
            pretty_print(f"Repository {repo_git_name} does not exist.", error=True)
            exit(1)
        os.chdir(repo_git_name)

    def _push_to_new_repo(self, repo_name: str, workspace: str):
        pretty_print("Pushing to new Bitbucket repository...")
        bb = Bitbucket()
        try:
            bb.push_to_mirror_repo(repo_name, workspace)
            pretty_print(f"Repository '{repo_name}' pushed to Bitbucket.")
        except BitbucketException as e:
            pretty_print(f"Error pushing: {e}", error=True)
            self._change_main_branch(workspace, repo_name)
            bb.push_to_mirror_repo(repo_name, workspace)
        bb.set_mirror_origin(repo_name, workspace)

    def _change_main_branch(self, workspace: str, repo_name: str):
        pretty_print("Opening Bitbucket admin to change default branch...")
        pw = BitbucketPlaywright()
        try:
            pw.ensure_logged_in()
            pw.page.goto(f"https://bitbucket.org/{workspace}/{repo_name}/admin")
            pw.page.wait_for_load_state("networkidle")
            pretty_print("Change the default branch to 'main', then press Enter.")
            input()
        finally:
            pw.close()
