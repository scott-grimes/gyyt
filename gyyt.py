#!/usr/bin/env python3
'''
A git clone
'''

from argparse import ArgumentParser
from resources.init import gyyt_init
commands = {
'add': '',
'cat-file': '',
'checkout': '',
'commit': '',
'hash-object': '',
'init': 'initalize a new, empty repo',
'log': '',
'ls-tree': '',
'merge': '',
'rebase': '',
'rev-parse': '',
'rm': '',
'show-ref': '',
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
    print(args)
    function(args)

def parse():
    parser = ArgumentParser(
        description='A git clone'
    )
    add_subparsers(parser)
    return parser.parse_args()

def add_subparsers(parser):
    subparser = parser.add_subparsers(dest='command')
    subparser.required = True

    init_parser = subparser.add_parser(
      'init',
      help=commands['init']
    )
    init_parser.add_argument(
       "path",
       metavar="directory",
       nargs="?",
       default=".",
       help="where to create the repository"
    )


if __name__ == '__main__':
    main()
