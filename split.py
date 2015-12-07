#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-08-20 00:22:49
# @Author  : Chuang Ding
# @Email   : dingchuangnwpu@hotmail.com
# @Usage   : split all to train test val

import os
import sys

def main():
    all_raw = sys.argv[1]
    train_raw = sys.argv[2]
    test_raw = sys.argv[3]
    val_raw = sys.argv[4]

    all_raw = open(all_raw,'r')
    train_raw = open(train_raw,'w')
    test_raw = open(test_raw,'w')
    val_raw = open(val_raw,'w')
    index = 1
    for line in all_raw:
        if index%10 == 0 and index%20 != 0:
            test_raw.write(line)
        elif index%20 == 0:
            val_raw.write(line)
        else:
            train_raw.write(line)
        index += 1

if __name__ == '__main__':
    main()
