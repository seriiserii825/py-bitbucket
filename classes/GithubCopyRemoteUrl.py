from classes.GithubClass import GithubClass
from classes.Clipboard import ClipboardManager
from classes.Notification import Notification
from execeptions.GithubException import GithubException
from utils import pretty_print, selectOne


class GithubCopyRemoteUrl:
    def __init__(self):
        self.start()

    def start(self):
        gh = GithubClass()
        try:
            username = gh._get_data_from_env("GITHUB_USERNAME")
            repo_name = gh._get_repo_from_file()[0]
            remote_url = f"git@github.com:{username}/{repo_name}.git"
            action = selectOne(["url only", "set", "add"])
            if action == "url only":
                clipboard_text = remote_url
            else:
                subcommand = "set-url" if action == "set" else "add"
                clipboard_text = f"git remote {subcommand} origin {remote_url}"
            ClipboardManager.write(clipboard_text)
            Notification.notify("Copied to clipboard", clipboard_text)
            pretty_print(f"Copied to clipboard: {clipboard_text}")
        except GithubException as e:
            pretty_print(f"Error: {e}", error=True)
