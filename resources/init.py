from . import utils
from . import objects
import configparser
import os

def default_config():
    '''
    git (and therefore gyyt) uses ini config
    '''
    config = configparser.ConfigParser()
    config.add_section("core")
    config.set("core", "repositoryformatversion", "0")
    config.set("core", "filemode", "false")
    config.set("core", "bare", "false")

    return config

def repo_create(path):
    '''
    instantiates a new repo at path
    '''

    repo = objects.GyytRepo(path, create=True)
    worktree = repo.worktree
    if not os.path.exists(worktree):
        os.makedirs(worktree)
    if not os.path.isdir(worktree):
        raise Exception(f'{worktree} is not a directory')
    if os.listdir(worktree):
        raise Exception(f'{worktree} is not empty')

    # create required directories

    assert(utils.repo_dir(repo, "branches", mkdir=True))
    assert(utils.repo_dir(repo, "objects", mkdir=True))
    assert(utils.repo_dir(repo, "refs", "tags", mkdir=True))
    assert(utils.repo_dir(repo, "refs", "heads", mkdir=True))

    # ./gyyt/description
    with open(utils.repo_file(repo, "description"), "w") as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

    # ./gyyt/HEAD
    with open(utils.repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    # ./gyyt/config
    with open(utils.repo_file(repo, "config"), "w") as f:
        config = default_config()
        config.write(f)

    return repo

def gyyt_init(args):
    '''
    instantiate the repo
    '''
    repo_create(args.path)
