#!/usr/bin/env python
# coding=utf-8

import os, argparse

parser = argparse.ArgumentParser(description= 
				 'List  information  about  the  FILEs (the current directory by default)')
parser.add_argument('files', metavar='File', default='.', nargs='*',
		    help='The files about which the information will be listed')

parser.add_argument('-a', '--all',action='store_true',
		    help='do not ignore entries starting with .')
parser.add_argument('-l', '--list',action='store_true',
		    help='use a long listing format ')
parser.add_argument('-R', '--recursive',action='store_true',
		    help='list subdirectories recursively')

args = parser.parse_args()

from lsR import *


if __name__ == '__main__':
    if args.recursive:
        lsR()
    else:
        if args.list :
            print('Total Size:',size())
            if args.all:
                lsa()
                for file in os.listdir():
                     lsl(file)
            else:
                for file in os.listdir():
                    if file[0] != '.':
                        lsl(file)
        else:
            if args.all:
                print('.'+'     '+'..',end = '    ')
            for file in os.listdir():
                if args.all:
                    print(file, end='    ')
                else:
                    if file[0] != '.':
                        print(file, end='    ')
    print()


  
  