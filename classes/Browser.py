import webbrowser


class Browser:
    def __init__(self, workspace, repo_name):
        self.workspace = workspace
        self.repo_name = repo_name

    def create_repo_in_browser(self):
        create_url = f"https://bitbucket.org/{self.workspace}\
        /workspace/create/repository"
        print("Create new repo in blueline-wordpress-sites")
        print(create_url)
        webbrowser.open(create_url)
        confirm = input(
            "Press 'y' when you finished to create: ")
        if confirm.lower() != 'y':
            print("Aborting...")
            exit(1)

    def edit_group_in_browser(self, workspace: str, repo_name: str):
        print("Add group to your Bitbucket account.")
        group_url = f"https://bitbucket.org/{workspace}\
        /{repo_name}/admin/permissions"
        print(group_url)
        webbrowser.open(group_url)
        confirm = input("Press 'y' when you have added the group: ")
        if confirm.lower() != 'y':
            print("Aborting...")
            exit(1)
