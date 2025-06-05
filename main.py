from classes.Bitbucket import Bitbucket
from classes.Github import Github
from classes.MySelenium import MySelenium
from rich import print

def menu():
    print("[green]1. Copy old repo to bitbucket2025")
    print("[green]1.1 Check repository")
    print("[blue]2. Create new repository")
    print("[blue]3. Clone new repository")
    print("[blue]4. Open permissions")
    print("[red]5. Delete old repo")
    print("[yellow]6. Search github")
    print("[yellow]7. Clone from github")


    choice = input("Enter your choice: ")
    bb = Bitbucket()

    if choice == "1":
        bb.setRepoName()
        bb.checkRepoOnOldAccount()
        bb.checkRepoOnNewAccount()
        bb.copyOldRepoToNew()
        want_to_clone = input("Do you want to clone the new repository? (y/n): ").strip().lower()
        if want_to_clone == 'y':
            bb.cloneNewRepo()
        else:
            print("[yellow]Skipping clone operation.")
    elif choice == "1.1":
        bb.setRepoName()
        bb.checkRepoOnOldAccount()
        bb.checkRepoOnNewAccount()
    elif choice == "2":
        bb.setRepoName()
        bb.checkRepoOnNewAccount()
        bb.newRepo()
    elif choice == "3":
        bb.setRepoName()
        bb.checkRepoOnNewAccount()
        bb.cloneNewRepo()
    elif choice == "4":
        bb.setRepoName()
        bb.checkForNewRepo()
        bb.openPermissionsInBrowser()
        exit()
    elif choice == "5":
        bb.setRepoName()
        bb.checkRepoOnOldAccount()
        bb.deleteRepo()
    elif choice == "6":
        gh = Github()
        gh.findRepo()
        menu()
    elif choice == "7":
        gh = Github()
        gh.setRepoName()
        gh.checkRepo()
        gh.cloneRepo()
    else:
        print("[red]Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
