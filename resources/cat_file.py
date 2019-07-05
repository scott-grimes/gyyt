from . import utils
import sys

def gyyt_cat_file(args):
    repo = utils.repo_find()
    cat_file(repo, args.object, fmt=args.type.encode())

def cat_file(repo, obj, fmt=None):
    obj = utils.obj_read(repo, utils.obj_find(repo, obj, fmt=fmt))
    sys.stdout.buffer.write(obj.serialize())
