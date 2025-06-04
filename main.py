from classes.Bitbucket import Bitbucket
from classes.MySelenium import MySelenium
from rich import print

def menu():
    print("[green]1. Clone old repository")
    print("[blue]2. Create new repository")
    print("[blue]3. Clone new repository")
    print("[green]4. Open permissions")
    print("[red]5. Exit")


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
        print("[red]Exiting...")
        exit()
    else:
        print("[red]Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
