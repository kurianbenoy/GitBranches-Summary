import os
import time
import git
from git import Repo
from collections import Counter
from functools import wraps
from pathlib import Path


def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        """Decorator Function used to calculate the time taken to run any function"""
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print(f"@timefn: {fn.__name__} took {t2-t1} seconds")
        return result

    return measure_time


@timefn
def get_branches(path: os.PathLike):
    """
    Entry point function which lists the various branch in the file path passed. The get_branches returns
    the branches in the existing code repository. This functions also calls the get_author_details functions within it.
    returns: branches
    """
    try:
        repo = Repo(path)
        branches = set()

        assert not repo.bare
        assert repo.branches
        for branch in repo.branches:
            branches.add(str(branch))
            print(f"Branch: {branch}")
            commit_branch_list = list(repo.iter_commits(branch))
            print(f"Total commits in {branch} branch :-> {len(commit_branch_list)}")
            get_author_details(repo, branch, commit_branch_list)

        return branches
    except:
        print("Error in something-> go to debugging state")


def get_author_details(repo, branch: str, commit_branch_list):
    """Function which gets the statistics of how many authors have commited in branch based
    on their username details. This implementation uses python dictionaries
    """
    author_details = {}
    for i in range(len(commit_branch_list)):
        commit = commit_branch_list[i]
        author_details[commit.author.name] = 0

    for i in range(len(commit_branch_list)):
        commit = commit_branch_list[i]
        author_details[commit.author.name] += 1

    print(author_details)

    return None


def get_author_details_list(repo, branch: str, commit_branch_list):
    """Function which gets the statistics of how many authors have commited in branch based
    on their username details. This implementation uses Lists with a counter.
    """
    author_details = []
    for i in range(len(commit_branch_list)):
        commit = commit_branch_list[i]
        author_details.append(commit.author.name)

    print(Counter(author_details))
    return None


if __name__ == "__main__":
    print(
        "Hello Hello! Welcome to Git branches project. Which github repo do you want to analyse your branches?"
    )
    print(
        "Options\n1) Your  current working directory\n2) Provide the Path to your from this folder\n3) Enter a github repository url"
    )
    option = int(input())
    if option == 1:
        get_branches(os.getcwd())
    elif option == 2:
        print(
            "Provide your path to the repo from this folder in Pathlib expected format"
        )
        path = input()

    elif option == 3:
        print("Enter a github repository")
        git_repo_path = input()
        print("Enter a file path of empty directory to store project repo")
        folder_path = input()
        git.Git(folder_path).clone(git_repo_path)
        folder = os.path.join(os.getcwd(), folder_path)
        git_cloned_project = os.path.join(folder, os.listdir(folder)[0])
        get_branches(git_cloned_project)

