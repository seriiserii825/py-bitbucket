from classes.ForgejoClass import ForgejoClass
from py_libs.Clipboard import Clipboard
from execeptions.ForgejoException import ForgejoException
from utils import pretty_print, selectOne


class ForgejoCopyRemoteUrl:
    def __init__(self, action: str | None = None):
        self.action = action
        self.start()

    def start(self):
        fj = ForgejoClass()
        try:
            full_name = fj._get_repo_from_file()
            protocol = selectOne(["ssh", "https"])
            if protocol == "ssh":
                remote_url = fj.ssh_url(full_name)
            else:
                remote_url = fj.https_url(full_name)
            action = self.action or selectOne(["url only", "set", "add"])
            if action == "url only":
                clipboard_text = remote_url
            else:
                subcommand = "set-url" if action == "set" else "add"
                clipboard_text = f"git remote {subcommand} origin {remote_url}"
            Clipboard.write(clipboard_text)
            pretty_print(f"Copied to clipboard: {clipboard_text}")
        except ForgejoException as e:
            pretty_print(f"Error: {e}", error=True)
