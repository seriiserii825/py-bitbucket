from classes.GithubClass import GithubClass
from classes.Clipboard import ClipboardManager
from classes.Notification import Notification
from execeptions.GithubException import GithubException
from utils import pretty_print


class GithubCopyRemoteUrl:
    def __init__(self):
        self.start()

    def start(self):
        gh = GithubClass()
        try:
            username = gh._get_data_from_env("GITHUB_USERNAME")
            repo_name = gh._get_repo_from_file()[0]
            remote_url = f"git@github.com:{username}/{repo_name}.git"
            ClipboardManager.write(remote_url)
            Notification.notify("Remote URL copied", remote_url)
            pretty_print(f"Copied to clipboard: {remote_url}")
        except GithubException as e:
            pretty_print(f"Error: {e}", error=True)
