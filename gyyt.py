#!/usr/bin/env python3
'''
A git clone
'''

from argparse import ArgumentParser
from resources.init import gyyt_init
from resources.cat_file import gyyt_cat_file
from resources.hash_object import gyyt_hash_object
commands = {
    'add': '',
    'cat_file': 'show content of repo object',
    'checkout': '',
    'commit': '',
    'hash_object': 'compute the sha of object, optionally create blob from the file',
    'init': 'initalize a new, empty repo',
    'log': '',
    'ls_tree': '',
    'merge': '',
    'rebase': '',
    'rev_parse': '',
    'rm': '',
    'show_ref': '',
    'tag': '',
}

def main():
    '''
    Main function which parses arguments and calls correct function
    '''
    args = parse()
    if args.command not in commands.keys():
        raise Exception(f'Invalid command "{args.command}", run gyyt -h for a list of commands')
    function = globals()[f'gyyt_{args.command}']
    function(args)

def parse():
    parser = ArgumentParser(
        description='A git clone')
    add_subparsers(parser)
    return parser.parse_args()

def add_subparsers(parser):
    subparser = parser.add_subparsers(dest='command')
    subparser.required = True

    init_parser = subparser.add_parser(
      'init',
      help=commands['init'])
    init_parser.add_argument(
       'path',
       metavar='directory',
       nargs='?',
       default='.',
       help='where to create the repository')

    cat_parser = subparser.add_parser(
        'cat_file',
        help=commands['cat_file'])
    cat_parser.add_argument('type',
       metavar='type',
       choices=['blob', 'commit', 'tag', 'tree'],
       help='specify the type')
    cat_parser.add_argument('object',
       metavar='object',
       help='the object to display')

    hash_obj_parser = subparser.add_parser(
    "hash_object",
    help=commands['hash_object'])

    hash_obj_parser.add_argument("-t",
                       metavar="type",
                       dest="fmt",
                       choices=["blob", "commit", "tag", "tree"],
                       default="blob",
                       required=True,
                       help="Specify the type")

    hash_obj_parser.add_argument("-w",
                       dest="write",
                       action="store_true",
                       help="write the object into the database")

    hash_obj_parser.add_argument("path",
                       help="read object from <file>")

if __name__ == '__main__':
    main()
