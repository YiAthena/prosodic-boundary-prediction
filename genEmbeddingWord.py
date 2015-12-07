#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-09-24 11:23:45
# @Author  : Chuang Ding
# @Email   : dingchuangnwpu@hotmail.com
# @Usage   : get one hot representation

import os
import sys

coding=3
prefix = "XXX"
suffix = "YYY"

def Usage():
    print sys.argv[0] + "dict_character punc_list set pw_in pw_out pph_in pph_out iph_in iph_out frame"

def get_context(line,cnt,ncontext):
    line = line.replace("1","")
    line = line.replace("2","")
    line = line.replace("3","")

    newline = line
    for i in xrange(0,ncontext):
        newline = prefix + newline + suffix
    cnt = cnt*coding + ncontext*coding
    c = newline[cnt - ncontext*coding:cnt + ncontext*coding + coding]
    return c


def get_embedding(context, voc, voc_vector, dim):
    if context in voc:
        loc = voc.index(context)
        return voc_vector[loc]
    else:
        zeros = ['0.0']*dim
        return ' '.join(zeros)

def get_onehot(context,dict_character):
    zeros = ['0']*len(dict_character)
    cnt = 0
    while cnt < len(context):
        c = context[cnt:cnt+coding]
        if dict_character.count(c) > 0:
            loc = dict_character.index(c)
            zeros[loc] = '1'
        cnt += coding
    
    onehot = ' '.join(zeros)
    #onehot = str(zeros[0])
    #for i in range(1,len(dict_character)):
    #    onehot += " " + str(zeros[i])
    return onehot
    
def main():
    fdict = open(sys.argv[1],"r")
    fpunc = open(sys.argv[2],"r")

    #dict_character = list()
    #for line in fdict:
    #    tokens = line.strip("\n\r").split("\t")
    #    dict_character.append(tokens[0])
    #fdict.close()
    
    #dict_character.append(prefix)    
    #dict_character.append(suffix)

    voc = list()
    voc_vector = list()
    cnt = 0
    dim = 0
    voc_size = 0
    for line in fdict:
        line = line.strip('\n\r')
        if cnt == 0:
            tokens = line.split(' ')
            voc_size = int(tokens[0])
            dim = int(tokens[1])
            cnt += 1
            continue
        loc = line.find(' ')
        voc.append(line[:loc])
        voc_vector.append(line[loc+1:])
        cnt += 1
    fdict.close()
    print str(voc_size) + ' ' + str(dim)

    punc_list = list()
    for line in fpunc:
        line = line.strip("\n\r")
        punc_list.append(line)
    fpunc.close()
    
    fpw_in = open(sys.argv[4],"w")
    fpw_out = open(sys.argv[5],"w")
    fpph_in = open(sys.argv[6],"w")
    fpph_out = open(sys.argv[7],"w")
    fiph_in = open(sys.argv[8],"w")
    fiph_out = open(sys.argv[9],"w")
    fframe = open(sys.argv[10],"w")
    ncontext = 0
    fset = open(sys.argv[3],"r")
    num_set = 0
    for line in fset:
        line = line.strip("\n\r")
        index = 0
        cnt = 0
        tag = "3"
        while index < len(line):
            context = get_context(line,cnt,ncontext)
            cnt += 1            
            #onehot = get_onehot(context,dict_character)
            onehot = get_embedding(context, voc, voc_vector, dim)
            index += 3
            
            # pw
            pw_in = onehot
            if tag == "1" or tag == "2" or tag == "3":
                pw_out = "1 0 0"
                pph_in = onehot + " 1.0"
            else:
                pw_out = "0 0 1"
                pph_in = onehot + " 0.0"
            # pph
            if tag == "2" or tag == "3":
                pph_out = "1 0 0"
                iph_in = onehot + " 1.0"
            else:
                pph_out = "0 0 1"
                iph_in = onehot + " 0.0"
            # iph
            if tag == "3":
                iph_out = "1 0 0"
            else:
                iph_out = "0 0 1"
            
            char = context[ncontext*3:ncontext*3+3]
            
            if punc_list.count(char) > 0:
                pw_out = "0 1 0"
                pph_out = "0 1 0"
                iph_out = "0 1 0"
            
            fpw_in.write(pw_in+"\n")
            fpw_out.write(pw_out+"\n")
            fpph_in.write(pph_in+"\n")
            fpph_out.write(pph_out+"\n")
            fiph_in.write(iph_in+"\n")
            fiph_out.write(iph_out+"\n")
            
            if index >= len(line):
                break
            if line[index] == "1" or line[index] == "2" or line[index] == "3":
                tag = line[index]
                index += 1
            else:
                tag = "0"
        fframe.write(str(cnt)+"\n")
        fpw_in.write("\n")
        fpw_out.write("\n")
        fpph_in.write("\n")
        fpph_out.write("\n")
        fiph_in.write("\n")
        fiph_out.write("\n")

        num_set += 1
        if num_set % 100 == 0:
            print num_set

    fpw_in.close()
    fpw_out.close()
    fpph_in.close()
    fpph_out.close()
    fiph_in.close()
    fiph_out.close()
        
if __name__ == '__main__':
    main()
