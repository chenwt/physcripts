#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print "usage: filter_phylip.py <infile> [excluded=<excludedtaxafile> | accepted=<acceptednamesfile>] <outfile>"
        sys.exit(0)

    infile = open(sys.argv[1],"r")
    outfile = open(sys.argv[3],"w")
    
    listtype, namesfile = sys.argv[2].split("=")
    

    if listtype == "excluded" or listtype == "included":
        names = [n.strip() for n in open(namesfile,"r").readlines()]
    else:
        print "unrecognized type for names list; please use 'excluded' or 'included'"
        sys.exit(0)

    while True:
        testline = infile.readline()
        try:
            ntax, nsites = [int(n) for n in testline.split()]
            break
        except IndexError:
            continue

    saved = list()

    for name, seq in [line.split() for line in infile]:

        if listtype == "excluded":
            if name in names:
                continue

        elif listtype == "included":
            if name not in names:
                continue

        saved.append(name + " " + seq + "\n")
        ntax -= 1

    outfile.write(str(ntax) + " " + str(nsites) + "\n")

    for line in saved:
        outfile.write(line);

    outfile.close()
