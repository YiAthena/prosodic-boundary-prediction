#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-08-20 14:40:34
# @Author  : Chuang Ding
# @Email   : dingchuangnwpu@hotmail.com
# @Usage   : eval CRF

import os
import sys
import numpy as np

def getIndex(index):
    if index == 'B':
        return 0
    if index == 'I':
        return 1
    if index == 'O':
        return 2

def main():
    result=open(sys.argv[1],'r')
    
    cm = np.zeros((3,3))
    token = 0
    for line in result:
        line = line.strip('\n\r')
        if len(line) == 0:
            cm[0,0] -= 1
            continue
        token += 1
        items = line.split()
        pred = getIndex(items[-1])
        real = getIndex(items[-2])
        cm[real,pred] += 1

    ans = cm[0,0] + cm[0,1] + cm[0,2]
    rst = cm[0,0] + cm[1,0] + cm[2,0]
    ans_rst = cm[0,0]
    
    print "token\tbound\tfind\tcorrect"
    print str(token) + '\t' + str(ans) + '\t' + str(rst) + '\t' + str(ans_rst)
    print "confusion matrix"
    for i in range(0,3):
        print str(cm[i,0]) + '\t' + str(cm[i,1]) + '\t' + str(cm[i,2])
    precision = 1.0 * ans_rst / rst
    recall = 1.0 * ans_rst / ans
    F1 = 2 * precision*recall / (precision + recall)
    print "precision\trecall\t\tF1"
    print "%.6f\t%.6f\t%.6f" %(precision,recall,F1)
    print

if __name__ == '__main__':
    main()
