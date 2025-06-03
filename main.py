from classes.Bitbucket import Bitbucket


def menu():
    print("1. Clone old repository")
    print("2. Create new repository")
    print("3. Open permissions in browser")
    print("4. Exit")

if __name__ == "__main__":
    bb = Bitbucket()
    bb.setRepoName()
    bb.checkRepoOnOldAccount()
    bb.checkRepoOnNewAccount()
    bb.createRepo()
    menu()
