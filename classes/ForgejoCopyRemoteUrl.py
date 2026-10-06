from classes.ForgejoClass import ForgejoClass
from py_libs.Clipboard import Clipboard
from execeptions.ForgejoException import ForgejoException
from utils import pretty_print, selectOne


class ForgejoCopyRemoteUrl:
    def __init__(self):
        self.start()

    def start(self):
        fj = ForgejoClass()
        try:
            remote_url = fj.ssh_url(fj._get_repo_from_file())
            action = selectOne(["url only", "set", "add"])
            if action == "url only":
                clipboard_text = remote_url
            else:
                subcommand = "set-url" if action == "set" else "add"
                clipboard_text = f"git remote {subcommand} origin {remote_url}"
            Clipboard.write(clipboard_text)
            pretty_print(f"Copied to clipboard: {clipboard_text}")
        except ForgejoException as e:
            pretty_print(f"Error: {e}", error=True)
