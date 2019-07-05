import os
import configparser
from . import utils

class GyytRepo():
  '''
  represents the repo at path,
  optionally create a new repo at path
  '''
  worktree = None
  gyytDir = None
  conf = None

  def __init__(self, path, create=False):
    self.worktree = path
    self.gyytDir = os.path.join(path, '.gyyt')

    if not (create or os.path.isdir(self.gyytDir)):
      raise Exception(f'Not a Git repository {path}')

    self.conf = configparser.ConfigParser()
    cf = utils.repo_file(self, 'config')

    if cf and os.path.exists(cf):
      self.conf.read([cf])
    elif not create:
      raise Exception('config file missing')

    if not create:
      vers = int(self.conf.get('core', 'repositoryformatversion'))
      if vers != 0:
        raise Exception(f'Unsupported repositoryformatversion {vers}')


class GyytObject():
    '''
    An object is a binary blob that conforms to the following:
    The object starts with a header that specifies it's type
    [blob, commit, tag, tree]
    followed by an ascii space (0x20), the size of the object in
    bytes (as ascii number), then null (0x00), then the contents
    of the object
    '''
    repo = None

    def __init__(self, repo, data=None):
        self.repo=repo

        if data != None:
            self.deserialize(data)

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def deserialize(self, data):
        pass
