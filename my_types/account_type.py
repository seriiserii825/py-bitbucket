from typing import NamedTuple


class AccountType(NamedTuple):
    email: str
    workspace: str
    project_key: str
    username: str
    api_token: str
    is_private: str
    workspaces: str = ""
