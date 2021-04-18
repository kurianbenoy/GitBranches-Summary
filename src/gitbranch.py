import os
from git import Repo

def get_branches(path: os.PathLike):
    try:
        repo = Repo(path)
        branches = {}
        authors = []

        assert not repo.bare # check if the repo is a bare repo
        for branch in repo.branches:
            list_commits = list(repo.iter_commits(branch))
            branches[str(branch)] = len(list_commits)
            print(len(list_commits))

        return branches
      
    except:
        print("No branches exist")


if __name__ == "__main__":
    print(get_branches(os.getcwd()))
