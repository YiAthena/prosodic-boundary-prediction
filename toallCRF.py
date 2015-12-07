#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015/08/22
# @Author  : Chuang Ding
# @Email   : dingchuangnwpu@hotmail.com
# @Usage   : to all CRF

import os
import sys

def main():
    result_all = open(sys.argv[1],'r')
    level = ''
    newline = ''
    for line in result_all:
        line = line.strip('\n\r')
        if len(line) == 0:
            print newline
            level = ''
            newline = ''
            continue
        items = line.split()
        
        pw = items[-3]
        pph = items[-2]
        iph = items[-1]
        
        if pw == 'B' and pph == 'B' and iph == 'B':
            level = '3'
        elif pw == 'B' and pph == 'B' and iph == 'I':
            level = '2'
        elif pw == 'B' and pph == 'I' and iph == 'I':
            level = '1'
        else:
            level = ''
        newline = newline + level + items[0]

if __name__ == '__main__':
    main()