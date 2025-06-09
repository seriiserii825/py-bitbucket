from typing import NamedTuple


class AccountType(NamedTuple):
    email: str
    workspace: str
    project_key: str
    username: str
    app_password: str
    is_private: str
