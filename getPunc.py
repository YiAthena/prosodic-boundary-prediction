#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-08-20 17:07:15
# @Author  : Chuang Ding
# @Email   : dingchuangnwpu@hotmail.com
# @Usage   : get punc list

import os
import sys

def main():
    pos = open(sys.argv[1],'r').readlines()

    punc = set()
    for line in pos:
        line = line.strip('\n\r')
        items = line.split()
        for item in items:
            word = item.split('_')[0]
            pos = item.split('_')[1]

            if pos == 'wp':
                punc.add(word)

    for p in punc:
        print p

if __name__ == '__main__':
    main()
