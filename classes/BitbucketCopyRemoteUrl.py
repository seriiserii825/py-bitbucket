from classes.Bitbucket import Bitbucket
from py_libs.Clipboard import Clipboard
from execeptions.BitbucketException import BitbucketException
from utils import pretty_print, selectOne


class BitbucketCopyRemoteUrl:
    def __init__(self, action: str | None = None):
        self.action = action
        self.start()

    def start(self):
        bb = Bitbucket()
        try:
            repo = bb.get_repo_from_file()
            protocol = selectOne(["ssh", "https"])
            if protocol == "ssh":
                remote_url = f"git@bitbucket.org:{repo.workspace}/{repo.name}.git"
            else:
                remote_url = f"https://bitbucket.org/{repo.workspace}/{repo.name}.git"
            action = self.action or selectOne(["url only", "set", "add"])
            if action == "url only":
                clipboard_text = remote_url
            else:
                subcommand = "set-url" if action == "set" else "add"
                clipboard_text = f"git remote {subcommand} origin {remote_url}"
            Clipboard.write(clipboard_text)
            pretty_print(f"Copied to clipboard: {clipboard_text}")
        except BitbucketException as e:
            pretty_print(f"Error: {e}", error=True)
