from newRepoData import newRepoData
from oldRepoData import oldRepoData


class MyConfig:
    def __init__(self):
        self.initNewData()
        self.initOldData()
        self.new_workspace = ""
        self.new_project_key = ""
        self.new_username = ""
        self.new_app_password = ""
        self.new_is_private = False
        self.new_login_name = "reggiocalor"
        self.new_password = "wenuB(q]X}Uj6sA]"
        self.old_workspace = ""
        self.old_project_key = ""
        self.old_username = ""
        self.old_app_password = ""
        self.old_is_private = False

    def initNewData(self):
        new_data = newRepoData()
        self.new_workspace = new_data["new_workspace"]
        self.new_project_key = new_data["new_project_key"]
        self.new_username = new_data["new_username"]
        self.new_app_password = new_data["new_app_password"]
        self.new_is_private = new_data["new_is_private"]
        self.bitbucket_login = new_data["bitbucket_login"]
        self.bitbucket_password = new_data["bitbucket_password"]

    def initOldData(self):
        old_data = oldRepoData()
        self.old_workspace = old_data["old_workspace"]
        self.old_project_key = old_data["old_project_key"]
        self.old_username = old_data["old_username"]
        self.old_app_password = old_data["old_app_password"]
        self.old_is_private = old_data["old_is_private"]

