#!/usr/bin/env python
# coding=utf-8

import os, argparse, stat, grp, time, sys, pwd
from stat import *

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
parser.add_argument('--sort',action='append',dest='sort_option',default=[],
                    help='''sort by Option instead of name: 'None', 'len', 'size', 'uid', 'gid', 'ctime', 'reverse', and so on...
                    'reverse' can be given as second args.''')

args = parser.parse_args() 

#
class Ls():
    def __init__(self, _a, _l, _R, _sort):
        self._a = _a
        self._l = _l
        self._R = _R
        self._sort(_sort)
    
    def _sort(self, _sort):
        try:
            if _sort[1]: self._sort.reverse = True
        except:
            self.reverse = False
        try:
            self.key = _sort[0]
        except:
            self.key = None
            
    def Judg_R(self):
        self.Judg_al()
        self.output()
        if self._R:
            for dir in os.listdir():
                if (not (os.path.islink(dir)) and os.path.isdir(dir)):
                    if self._a:
                        os.chdir(dir)
                        self.Judg_R()
                        os.chdir('..')
                    else:
                        if dir[0] != '.':
                            os.chdir(dir)
                            self.Judg_R()
                            os.chdir('..')
        return
        
    def Judg_al(self):
        self._files = []
        for file in os.listdir():
            self._files.append([file])
        if self._a: self._files = [['.'], ['..']] + self._files
        for num in range(len(self._files)):
            self.get_stat(self._files[num], num)
        else:
            self.output_rjust()
    
    def get_stat(self, file, num):
        file = file[-1]
        try:
            mode = self.get_mode(file)
            link = str(os.stat(file).st_nlink)
            try:
                uid = pwd.getpwuid(os.stat(file).st_uid).pw_name
            except:
                uid = str(os.stat(file).st_uid)
            try:
                gid = grp.getgrgid(os.stat(file).st_gid).gr_name
            except:
                gid = str(os.stat(file).st_gid)
        
            size = str(os.stat(file).st_size)
            ctime = time.ctime(os.stat(file).st_ctime)
        except:
            mode, link, uid, gid ,size, ctime= '----------', '0', '0', '0', '0', '0'    #错误处理,跳过无法查询到stat的文件
        if ctime[-4:] == time.ctime()[-4:]:  #年代不为今年则显示年份
            ctime = ctime[4:-8]
        else:
            ctime = ctime[4:]
            
        self._files[num] = [mode, link, uid, gid, size, ctime, file]
    
    def output_rjust(self):
        len_link = len_uid = len_gid = len_size = len_size =  0
        len_list = [len_link, len_uid, len_gid, len_size, len_size ]
        for i in self._files:
            for n in [1,2,3,4,5]:
                if len(i[n]) > len_list[n-1]: len_list[n-1] = len(i[n])
        
        for num in self._files:
            for i in [1,4,5]:
                num[i] = num[i].rjust(len_list[i-1])
            for i in [2,3]:
                num[i] = num[i].ljust(len_list[i-1])
        
        
    def output(self):
        self.sort()
        if self._R: 
            try:
                print('\033[1;33;40m'+os.getcwd()+'\033[0m'+':')
            except:
                print("name of files can't be loaded")
        if self._l:
            print('Total Size: '+str(self.total_size()))
            for i in self._files: 
                n = 0
                for ii in i:
                    n += 1
                    try:
                        if n == 7:
                            if os.path.isdir(i[n-1]):
                                print('\033[1;34;40m',end='')
                        else:
                            print('\033[0m',end='')
                        if self._a:
                            print(ii + '\033[0m', end =' ')
                        else:
                            if i[6][0] != '.':
                                print(ii + '\033[0m', end =' ')
                    except:
                        print("Aname of files can't be loaded"+'\033[0m')
                if (not self._a) and i[6][0] !='.':print()
                if self._a: print()
        else:
            try:
                for i in self._files: 
                    if os.path.isdir(i[-1]):
                        print('\033[1;34;40m',end='')
                    if not self._a:
                        if i[-1][0] != '.':
                            print(i[-1], '\033[0m',end= '   ')
                    else:
                         print(i[-1], '\033[0m',end= '   ')
            except:
                print("name of files can't be loaded"+'\033[0m',end='')
        if not self._l: print()
        if self._R: print() #修正输出: 最后回车
        
    
    def sort(self):
        try:
            if self.key == 'None' or self.key == 'none' or self.key == None:
                self._files.sort(reverse= self.reverse)
            elif self.key == 'len': self._files.sort(key = lambda x:len(x[-1]), reverse= self.reverse)
            else:
                key = {'size':4, 'uid':2, 'gid':3, 'ctime':5, 'link':1, 'name':6}
                self._files.sort(key = lambda x:x[key[self.key]], reverse= self.reverse)
        except:
            print("Option do not have definition.You can try 'none','name','len','uid','gid','ctime'.")
    
    def get_mode(self, file):
        try:
            x = oct(os.stat(os.path.abspath(file))[ST_MODE])[-3:]
        except:
            a = '----------'
            return a
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
    
    def total_size(self):#求文件夹大小
        def size_R():
            size = 0
            for file in os.listdir():
                if (not os.path.islink(file)) and os.path.isfile(file):
                    size += os.stat(file).st_size
                #if (not os.path.islink(file)) and os.path.isdir(file):
                #    os.chdir(file)
                #    size_R()
                #    os.chdir('..')
            return size
        return size_R()


if __name__ == '__main__':
    _cwd = os.getcwd()
    for i in args.files:
        os.chdir(i)
        if len(args.files) > 1:print('\033[1;32;40m'+i+'\033[0m')
        ls = Ls(args.all, args.list, args.recursive, args.sort_option)
        ls.Judg_R()
        os.chdir(_cwd)

