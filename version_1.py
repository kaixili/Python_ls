#!/usr/bin/env python
# coding=utf-8
'''
'''

import os, pwd, grp, time, sys
from stat import *


#判断-R的函数
def f():
    if R :
        print(os.getcwd())
        for i in os.listdir():
            lsl(i)
        print('\n')
        for i in os.listdir():
            if a == False:
                if i[0] != '.':
                    if os.path.isdir(i):
                        if os.path.islink(i):
                            pass
                        else:
                            os.chdir(i)
                            f()
                            os.chdir('..')
            else:
                if os.path.isdir(i):
                    if os.path.islink(i):
                        pass
                    else:
                        os.chdir(i)
                        f()
                        os.chdir('..')
    else:
        for i in os.listdir():
            lsl(i)
    return

def mod(i):#判断文件的权限
    x = oct(os.stat(os.path.abspath(i))[ST_MODE])[-3:]
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
    if os.path.isdir(i):
        mode = 'd' + mode
        dir_ = 0
    elif os.path.isfile(i):
        mode = '-' + mode
    elif os.path.islink(i):
        mode = 'l' + mode
    else:
        if i[0] != 's':
            mode = 'c' + mode
        else:
            mode = 'b' + mode
#输出函数
def lsl(i):
    if l :
        try:
            mod(i)
        except:
            print('cannot read a file!')
        if a :  #判断-a 来输出隐藏文件
            print(mode, "%3d"%(os.stat(i).st_nlink), pwd.getpwuid(os.stat(i)[4])[0], grp.getgrgid(os.stat(i)[5])[0],"%6d"%(os.stat(i)[6]), time.ctime(os.path.getmtime(i))[4:-8], i)
        else:
            if i[0] != '.':
                print(mode, "%3d"%(os.stat(i).st_nlink), pwd.getpwuid(os.stat(i)[4])[0], grp.getgrgid(os.stat(i)[5])[0],"%6d"%(os.stat(i)[6]), time.ctime(os.path.getmtime(i))[4:-8], i)
    else:
        if a :
            print(i, end='    ')
        else:
            if i[0] != '.':
                print(i , end='    ')

#参数处理

a = l = R =last=False
try:
    if ('a' in list(sys.argv[1]) or '-a' in sys.argv):
        a = True
    if ('l' in list(sys.argv[1]) or '-l' in sys.argv):
        l = True
    if ('R' in list(sys.argv[1]) or '-R' in sys.argv):
        R = True
except:
    last = True

f()
if (a or last):
    print()
