from classes.Bitbucket import Bitbucket
from classes.MySelenium import MySelenium


def menu():
    print("1. Clone old repository")
    print("2. Create new repository")
    print("3. Exit")


    choice = input("Enter your choice: ")
    bb = Bitbucket()

    if choice == "1":
        bb.setRepoName()
        bb.checkRepoOnOldAccount()
        bb.checkRepoOnNewAccount()
        bb.copyOldRepoToNew()
    elif choice == "2":
        bb.setRepoName()
        bb.checkRepoOnNewAccount()
        bb.createRepo()

    elif choice == "3":
        print("Exiting...")
        exit()
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
