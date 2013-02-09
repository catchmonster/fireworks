#!/usr/bin/env python

'''
A runnable script for managing a FireWorks database (a command-line interface to launchpad.py)
'''
from argparse import ArgumentParser
from fireworks.core.launchpad import LaunchPad
from fireworks.core.firework import FireWork
import ast

#TODO: YAML queries give weird unicode string, maybe this is unfixable though

__author__ = 'Anubhav Jain'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Anubhav Jain'
__email__ = 'ajain@lbl.gov'
__date__ = 'Feb 7, 2013'

if __name__ == '__main__':
    m_description = 'This script is used for creating and managing a FireWorks database. For a list \
    of available commands, type "launchpad_run.py -h". For more help on a specific command, type \
    "launchpad_run.py <command> -h".'
    
    parser = ArgumentParser(description=m_description)
    subparsers = parser.add_subparsers(help='command', dest='command')
    
    initialize_parser = subparsers.add_parser('initialize', help='initialize a FireWorks database')
    initialize_parser.add_argument('password', help="Today's date, e.g. 2012-02-25. Required to prevent \
    against accidental initializations.")
    
    upsert_parser = subparsers.add_parser('upsert_fw', help='insert or update a FireWork from file')
    upsert_parser.add_argument('fw_file', help="path to a FireWorks file")
    
    get_fw_parser = subparsers.add_parser('get_fw', help='get a FireWork by id')
    get_fw_parser.add_argument('fw_id', help="FireWork id", type=int)
    get_fw_parser.add_argument('-f', '--filename', help='output filename', default=None)
    
    get_fw_ids_parser = subparsers.add_parser('get_fw_ids', help='get FireWork ids by query')
    get_fw_ids_parser.add_argument('-q', '--query', help='query (as pymongo string, enclose in single-quotes)', default=None)
    
    parser.add_argument('-l', '--launchpad_file', help='path to launchpad file', default=None)
    
    args = parser.parse_args()
    
    if args.launchpad_file:
        lp = LaunchPad.from_file(args.launchpad_file)
    else:
        lp = LaunchPad()
    
    if args.command == 'initialize':
        lp.initialize(args.password)
    
    elif args.command == 'upsert_fw':
        fw = FireWork.from_file(args.fw_file)
        lp.upsert_fw(fw)
        
    elif args.command == 'get_fw':
        fw = lp.get_fw_by_id(args.fw_id)
        if args.filename:
            fw.to_file(args.filename)
        else:
            print fw.to_format('json', indent=4)
        
    elif args.command == 'get_fw_ids':
        if args.query:
            args.query = ast.literal_eval(args.query)
        print lp.get_fw_ids(args.query)