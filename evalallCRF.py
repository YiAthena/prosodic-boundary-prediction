#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015/08/22
# @Author  : Chuang Ding
# @Email   : dingchuangnwpu@hotmail.com
# @Usage   : eval all CRF

import os
import sys
import numpy as np

coding = 3

def getlevel(s):
    if s == '1':
        return 1
    elif s == '2':
        return 2
    elif s == '3':
        return 3
    else:
        return 0
    
def del_punc(line,punc):
    for p in punc:
        line = line.replace(p,'')
    return line
    

def main():
    lpred_rhy = open(sys.argv[2],'r').readlines()
    lreal_rhy = open(sys.argv[1],'r').readlines()
    lpunc = open(sys.argv[3],'r')
    punc = list()
    for line in lpunc:
        line = line.strip('\n\r')
        punc.append(line)
    
    index = 0
    cm = np.zeros((4,4))
    while index < len(lpred_rhy):
        pred_rhy = lpred_rhy[index].strip('\n\r')
        pred_rhy = del_punc(pred_rhy,punc)
        if pred_rhy[0] == '3' or pred_rhy[0] == '2':
            pred_rhy = pred_rhy[1:]
        real_rhy = lreal_rhy[index].strip('\n\r')
        real_rhy = del_punc(real_rhy,punc)
        pred_index = 0
        real_index = 0
        
        level_real = 0
        level_pred = 0
        #cm[3,3] = cm[3,3] - 1
        newline = ''
        while pred_index <= len(pred_rhy) - coding:
            c_real = real_rhy[real_index:real_index+coding]
            c_pred = pred_rhy[pred_index:pred_index+coding]
            if c_real == c_pred:
                if pred_index < len(pred_rhy) - coding:
                    level_real = getlevel(real_rhy[real_index+coding])
                    level_pred = getlevel(pred_rhy[pred_index+coding])
                    cm[level_real,level_pred] += 1
                    if level_real > 0:
                        real_index += 1
                    if level_pred > 0:
                        pred_index += 1
                else:
                    level_real = 3
                    level_pred = 3
                    #cm[level_real,level_pred] += 1
            else:
                print "ERROR:\n"+real_rhy+'\n'+pred_rhy
            real_index += coding
            pred_index += coding
            newline = newline + c_real + '/' + str(level_real) + str(level_pred)
        #print newline
        index += 1
    
    cm[1,1] = sum(sum(cm[1:,1:]))
    cm[2,2] = sum(sum(cm[2:,2:]))
    for i in range(0,4):
        print str(cm[i,0]) + '\t' + str(cm[i,1]) + '\t' + str(cm[i,2]) + '\t' + str(cm[i,3])
    
    sets = ('x','pw','pph','iph')
    for i in range(1,4):
        ans = sum(cm[i,0:i+1])
        rst = sum(cm[0:i+1,i])
        ans_rst = cm[i,i]
        precision = 1.0 * ans_rst / rst
        recall = 1.0 * ans_rst / ans
        F1 = 2 * precision*recall / (precision + recall)
        print sets[i]+":\tprecision\trecall\t\tF1"
        print "\t%.6f\t%.6f\t%.6f" %(precision,recall,F1)

if __name__ == '__main__':
    main()