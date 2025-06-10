from classes.Bitbucket import Bitbucket
from execeptions.BitbucketException import BitbucketException
from utils import pretty_print


class BitbucketFindRepoInFile:
    def start(self):
        bb = Bitbucket()
        try:
            bb.find_repo_in_file()
        except BitbucketException as e:
            pretty_print(f"Error: {e}", error=True)
