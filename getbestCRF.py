#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-08-20 14:40:34
# @Author  : Chuang Ding
# @Email   : dingchuangnwpu@hotmail.com
# @Usage   : get best for CRF

import os
import sys

def main():
    result=open(sys.argv[1],'r')
    
    term_index = 1
    line_index = 1
    train_F1 = list()
    val_F1 = list()
    test_F1 = list()
    f = list()
    c = list()
    for line in result:
        line = line.strip('\n\r')
        if len(line) == 0:
            term_index += 1
            line_index += 1
            continue
        if line_index % 30 == 1:
            items = line.split()
            f.append(items[0])
            c.append(items[1])
        if line_index % 10 == 9:
            items = line.split()
            if term_index % 3 == 1:
                train_F1.append(float(items[-1]))
            if term_index % 3 == 2:
                val_F1.append(float(items[-1]))
            if term_index % 3 == 0:
                test_F1.append(float(items[-1]))
        line_index += 1
    
    train_max_F1 = max(train_F1)
    index = train_F1.index(train_max_F1)
    print 'train:\t' + f[index] + '\t' + c[index] + '\t' + str(train_max_F1)
    
    val_max_F1 = max(val_F1)
    index = val_F1.index(val_max_F1)
    print 'val:\t' + f[index] + '\t' + c[index] + '\t' + str(val_max_F1)
    
    test_max_F1 = max(test_F1)
    index = test_F1.index(test_max_F1)
    print 'test:\t' + f[index] + '\t' + c[index] + '\t' + str(test_max_F1)

if __name__ == '__main__':
    main()
