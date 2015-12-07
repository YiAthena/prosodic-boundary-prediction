#!/usr/bin/env python

import os
import sys

_DEBUG=False
if _DEBUG == True:
    import pdb
    pdb.set_trace()

xml=open(sys.argv[1],"r");

for line in xml:
    s1 = "<word id="
    if line.find(s1)!=-1:
        flag=1;
        s2 = "cont=""";
        s3 = """ pos=""";
        s4 = """ />""";
        n2 = line.find(s2)
        n3 = line.find(s3)
        n4 = line.find(s4)
        #print line[n2+6:n3-1]+"/"+line[n3+6:n4-1],
        #print line[n2+6:n3-1],
        print line[n2+6:n3-1]+"_"+line[n3+6:n4-1],
    if line.find("</xml4nlp>")!=-1:
        print
