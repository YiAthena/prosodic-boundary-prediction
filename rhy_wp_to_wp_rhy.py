#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-08-20 17:07:15
# @Author  : Chuang Ding
# @Email   : dingchuangnwpu@hotmail.com
# @Usage   : mv rhy after wp

import os
import sys

def main():
    lrhy = open(sys.argv[1],'r').readlines()
    lpunc = open(sys.argv[2],'r').readlines()
    
    puncs = list()
    for line in lpunc:
        line = line.strip('\n\r')
        puncs.append(line)

    for line in lrhy:
        line = line.strip('\n\r')
        index = 0
        new_rhy = ''
        rhy = ''
        while index <= len(line) - 3:
            c = line[index:index+3]
            if not c in puncs:
                new_rhy = new_rhy + rhy + c
                rhy = line[index+3]
                if rhy == '1' or rhy == '2' or rhy == '3':
                    index += 1
                else:
                    rhy = ''
                index += 3
            else:
                while c in puncs:
                    new_rhy = new_rhy + c
                    index += 3
                    c = line[index:index+3]
        print new_rhy

if __name__ == '__main__':
    main()
