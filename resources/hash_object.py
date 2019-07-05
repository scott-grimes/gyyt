from . import utils
from . import objects
import sys

def gyyt_hash_object(args):
    repo =  objects.GyytRepo('.') if args.write else None
    with open(args.path, 'rb') as f:
        sha = obj_hash(f, args.fmt.encode(), repo = repo)
        if not args.write:
            print(sha)
def obj_hash(file, fmt, repo):
    data = file.read()

    if   fmt==b'commit' : obj=objects.GyytCommit(repo, data)
    elif fmt==b'tree'   : obj=objects.GyytTree(repo, data)
    elif fmt==b'tag'    : obj=objects.GyytTag(repo, data)
    elif fmt==b'blob'   : obj=objects.GyytBlob(repo, data)
    else:
        raise Exception(f'Unknown type {fmt}')
    # only write if a repo was given
    write = repo is not None
    return utils.obj_write(obj, write = write)
