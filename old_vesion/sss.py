#!/usr/bin/env python
# coding=utf-8

import argparse

import os, stat, grp, time, sys, pwd
from stat import *



def lsR():
    print()
    print('\033[1;32;40m'+ os.getcwd() +':', '\033[1;33;40m')
    print('Total Size:', size(),'\033[0m')
    if args.all:
        lsa()
    for file in os.listdir():
        lsl(file)    
    for dir in os.listdir():
        if (not (stat.S_ISLNK(os.stat(dir).st_mode)) and \
                stat.S_ISDIR(os.stat(dir).st_mode)):
            os.chdir(dir)
            lsR()
            os.chdir('..')
    return 

#判断文件的权限
def mod(file):
    x = oct(os.stat(os.path.abspath(file))[ST_MODE])[-3:]
    global mode
    mode = ''
    for ii in x:
        if bin(int(ii))[-3:][0] == '1':
            mode = mode + 'r'
        else:
            mode = mode + '-'
        if bin(int(ii))[-3:][1] == '1':
            mode = mode + 'w'
        else:
            mode = mode + '-'
        if bin(int(ii))[-3:][2] == '1':
            mode = mode + 'x'
        else:
            mode = mode + '-'
    ST = os.stat(file).st_mode
    if stat.S_ISREG(ST):
        mode = '-' + mode
    elif stat.S_ISDIR(ST):
        mode = 'd' + mode
    elif stat.S_ISLNK(ST):
        mode = 'l' + mode
    elif stat.S_ISBLK(ST):
        mode = 'b' + mode
    elif stat.S_ISCHR(ST):
        mode = 'c' + mode
    elif stat.S_ISSOCK(ST):
        mode = 's' + mode             
    elif stat.S_ISFIFO(ST):
        mode = 'p' + mode
    else:
        mode = '?' + mode
    return mode

#获得文件的大小
def size():
    def size_R():
        size = 0
        for file in os.listdir():
            if stat.S_ISREG(os.stat(file).st_mode):
                size += os.stat(file).st_size
            if stat.S_ISDIR(os.stat(file).st_mode):
                os.chdir(file)
                size_R()
                os.chdir('..')
        return size
    return size_R()

#输出-aR下的‘.’和‘..’
def lsa():
    '''print . and ..'''
    if args.list:
        first = os.getcwd()
        print(mod(first), "%3d"%(os.stat(first).st_nlink), pwd.getpwuid(os.stat(first).st_uid)[0], grp.getgrgid(os.stat(first).st_gid)[0], "%6d"%(os.stat(first).st_size),  time.ctime(os.path.getmtime(first))[4:-8],'\033[1;36;40m'+ '.' + '\033[0m')
        os.chdir('..')
        second = os.getcwd()
        os.chdir(first)
        print(mod(second), "%3d"%(os.stat(second).st_nlink), pwd.getpwuid(os.stat(second).st_uid)[0], grp.getgrgid(os.stat(second).st_gid)[0], "%6d"%(os.stat(second).st_size),  time.ctime(os.path.getmtime(second))[4:-8],'\033[1;36;40m'+ '..' + '\033[0m')
    else:
        print('.','    ','..', end = '     ')





#输出
def lsl(file):
    if args.list:
        if os.path.isdir(file):#文件夹颜色输出
            print(mod(file), "%3d"%(os.stat(file).st_nlink), pwd.getpwuid(os.stat(file).st_uid)[0], grp.getgrgid(os.stat(file).st_gid)[0], "%6d"%(os.stat(file).st_size),  time.ctime(os.path.getmtime(file))[4:-8],'\033[1;36;40m'+ file + '\033[0m')
        else:
            print(mod(file), "%3d"%(os.stat(file).st_nlink), pwd.getpwuid(os.stat(file).st_uid)[0], grp.getgrgid(os.stat(file).st_gid)[0], "%6d"%(os.stat(file).st_size),  time.ctime(os.path.getmtime(file))[4:-8], file)
    else:
        if args.all:
            print(file, end='    ')
        else:
            if file[0] != '.':
                print(file, end='    ')
    


##################################
#程序开始

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

if args.recursive: #判断-R
    lsR()          #-R成立后 -a-l的判断 交给了lsR()
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







