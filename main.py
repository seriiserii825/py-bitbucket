from classes.Bitbucket import Bitbucket


def menu():
    # print("[green]1. Show repo with fzf")
    # print("[green]2. Search repo by word")
    # print("[green]1. Copy old repo to bitbucket2025")
    # print("[green]1.1 Check repository")
    # print("[blue]2. Create new repository")
    # print("[blue]3. Clone new repository")
    # print("[blue]4. Open permissions")
    # print("[red]5. Delete old repo")
    # print("[yellow]6. Search github")
    # print("[yellow]7. Clone from github")
    # print("[yellow]8. Create repo github")
    # print("[blue]9. List repos")

    bb = Bitbucket('bludelego@gmail.com')
    bb.init_repo_data()

    # bb.initData(old_email)
    # bb.chooseWorkspaces()
    # # bb.showRepos()
    # bb.searchRepo()

    # if choice == "1":
    #     pass
    # elif choice == "2":
    #     pass

    # if choice == "1":
    #     bb.setRepoName()
    #     bb.checkRemoteRepo(old_workspace)
    #     bb.checkRemoteRepo(new_workspace, 2)
    #     bb.copyOldRepoToNew()
    #     want_to_clone = input("Do you want to clone the new repository? (y/n): ").strip().lower()
    #     if want_to_clone == 'y':
    #         bb.cloneNewRepo()
    #     else:
    #         print("[yellow]Skipping clone operation.")
    # elif choice == "1.1":
    #     bb.setRepoName()
    #     bb.checkRepoOnOldAccount()
    #     bb.checkRepoOnNewAccount()
    # elif choice == "2":
    #     bb.setRepoName()
    #     bb.checkRepoOnNewAccount()
    #     bb.newRepo()
    # elif choice == "3":
    #     bb.setRepoName()
    #     bb.checkRepoOnNewAccount()
    #     bb.cloneNewRepo()
    # elif choice == "4":
    #     bb.setRepoName()
    #     bb.checkForNewRepo()
    #     bb.openPermissionsInBrowser()
    #     exit()
    # elif choice == "5":
    #     bb.setRepoName()
    #     bb.checkRepoOnOldAccount()
    #     bb.deleteRepo()
    # elif choice == "6":
    #     gh = Github()
    #     gh.findRepo()
    #     menu()
    # elif choice == "7":
    #     gh = Github()
    #     gh.setRepoName()
    #     gh.checkRepo()
    #     gh.cloneRepo()
    # elif choice == "8":
    #     gh = Github()
    #     gh.createRepo()
    # elif choice == "9":
    #     bb = Bitbucket()
    #     workspaces = ['blueline2025']
    #     bb.fetchWorkspaceRepos(workspaces, 2)
    # else:
    #     print("[red]Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()
