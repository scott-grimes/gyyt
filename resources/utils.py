import os
import configparser

def repo_path(repo, *path):
  '''
  determine path in repo gyytdir
  '''
  return os.path.join(repo.gyytDir, *path)

def repo_file(repo, *path, mkdir=False):
  '''
  create and/or get a path to a file in repo gyytdir
  '''
  if repo_dir(repo, *path[:-1], mkdir=mkdir):
    return repo_path(repo, *path)

def repo_dir(repo, *path, mkdir=False):
  '''
  create and/or get a path to a directory in repo gyytdir
  '''
  path = repo_path(repo, *path)

  if os.path.exists(path):
    if not os.path.isdir(path):
      raise Exception(f'"{path}" is not a directory')
    return path
  if mkdir:
    os.makedirs(path)
    return path

def repo_find(path=".", required=True):
    '''
    from whatever path you're on, recurse back to /
    until you find the .gyyt directory
    '''
    path = os.path.realpath(path)

    if os.path.isdir(os.path.join(path, ".gyyt")):
        return GyytRepo(path)

    # will recurse in parent
    parent = os.path.realpath(os.path.join(path, ".."))

    # recursed to root dir
    if parent == path:
        if required:
            raise Exception("not a gyyt directory")
        else:
            return None

    return repo_find(parent, required)

def object_read(repo, sha):
    '''
    read object object_id from the repo.  Return a
    GyytObject whose type depends on the object
    '''

    path = repo_file(repo, "objects", sha[0:2], sha[2:])

    with open (path, "rb") as f:
        raw = zlib.decompress(f.read())

        #determine object type
        null_byte = raw.find(b' ')
        obj_header = raw[0:null_byte]

        # validate object size
        y = raw.find(b'\x00', x)
        size = int(raw[x:y].decode("ascii"))
        if size != len(raw)-y-1:
            raise Exception(f'malformed object {sha}: bad length')

        # construct object based on type
        if   obj_header==b'commit' : obj=GitCommit
        elif obj_header==b'tree'   : obj=GitTree
        elif obj_header==b'tag'    : obj=GitTag
        elif obj_header==b'blob'   : obj=GitBlob
        else:
            raise Exception(f"Unknown type {obj_header.decode('ascii')} for object {sha}")

        return obj(repo, raw[y+1:])
