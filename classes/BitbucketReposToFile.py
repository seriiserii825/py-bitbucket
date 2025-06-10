from classes.Bitbucket import Bitbucket


class BitbucketReposToFile:
    def start(self):
        bb = Bitbucket()
        bb.repos_to_file()
