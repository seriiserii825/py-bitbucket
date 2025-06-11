from classes.Bitbucket import Bitbucket
from utils import pretty_print


class BitbucketReposToFile:
    def __init__(self):
        pretty_print("Fetching Bitbucket Repositories to File")
        self.start()

    def start(self):
        bb = Bitbucket()
        bb.repos_to_file()
