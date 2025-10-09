from classes.Bitbucket import Bitbucket
from classes.Browser import Browser
from classes.Clipboard import ClipboardManager
from classes.Notification import Notification
from utils import pretty_print


class BitbucketCreateRepo:
    def __init__(self):
        self.start()

    def start(self):
        repo_name = self._set_repo_name()
        ClipboardManager.write(repo_name)
        Notification.notify("Repo name copied to clipboard", repo_name)
        workspace = self._select_workspace()
        self.browser_create_and_edit_group(workspace, repo_name)

    def _set_repo_name(self) -> str:
        pretty_print("Set repo name")
        bb = Bitbucket()
        return bb.set_repo_name()

    def _select_workspace(self) -> str:
        pretty_print("Select workspace")
        bb = Bitbucket()
        return bb.select_workspace()

    def browser_create_and_edit_group(self, workspace: str, repo_name: str):
        pretty_print("Create and edit group in browser")
        bw = Browser(workspace, repo_name)
        bw.create_repo_in_browser()
        bw.edit_group_in_browser(workspace, repo_name)
