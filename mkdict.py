#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

coding=3

def main():
    fprosody = open(sys.argv[1],"r")
    dict_character = open(sys.argv[2],"w")
    freq = sys.argv[3]

    set_character = set()
    list_character = list()
    for line in fprosody:
        line = line.strip("\n\r")
        i = 0
        while i < len(line):
            if line[i] == "1" or line[i] == "2" or line[i] == "3":
                i += 1
                continue
            else:
                set_character.add(line[i:i+coding])
                list_character.append(line[i:i+coding])
                i += coding

    l = list(set_character)
    l.sort()

    for c in l:
        num = list_character.count(c)
        if num >= int(freq):
            dict_character.write(c + "\t" + str(num) + "\n")

    fprosody.close()
    dict_character.close()

if __name__ == '__main__':
    main()
