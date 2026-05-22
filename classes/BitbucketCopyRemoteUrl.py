from classes.Bitbucket import Bitbucket
from classes.Clipboard import ClipboardManager
from classes.Notification import Notification
from execeptions.BitbucketException import BitbucketException
from utils import pretty_print


class BitbucketCopyRemoteUrl:
    def __init__(self):
        self.start()

    def start(self):
        bb = Bitbucket()
        try:
            repo = bb.get_repo_from_file()
            remote_url = f"git@bitbucket.org:{repo.workspace}/{repo.name}.git"
            ClipboardManager.write(remote_url)
            Notification.notify("Remote URL copied", remote_url)
            pretty_print(f"Copied to clipboard: {remote_url}")
        except BitbucketException as e:
            pretty_print(f"Error: {e}", error=True)
