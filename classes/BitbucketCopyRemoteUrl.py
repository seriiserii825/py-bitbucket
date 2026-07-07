from classes.Bitbucket import Bitbucket
from classes.Clipboard import ClipboardManager
from classes.Notification import Notification
from execeptions.BitbucketException import BitbucketException
from utils import pretty_print, selectOne


class BitbucketCopyRemoteUrl:
    def __init__(self):
        self.start()

    def start(self):
        bb = Bitbucket()
        try:
            repo = bb.get_repo_from_file()
            remote_url = f"git@bitbucket.org:{repo.workspace}/{repo.name}.git"
            action = selectOne(["url only", "set", "add"])
            if action == "url only":
                clipboard_text = remote_url
            else:
                subcommand = "set-url" if action == "set" else "add"
                clipboard_text = f"git remote {subcommand} origin {remote_url}"
            ClipboardManager.write(clipboard_text)
            Notification.notify("Copied to clipboard", clipboard_text)
            pretty_print(f"Copied to clipboard: {clipboard_text}")
        except BitbucketException as e:
            pretty_print(f"Error: {e}", error=True)
