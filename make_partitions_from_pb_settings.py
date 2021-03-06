#!/usr/bin/env python

if __name__ == '__main__':

    import sys
    from copy import deepcopy

    if len(sys.argv) < 3:
        print "usage: makepartitionsfrompbsettings <alignmentphy> <pbparamfile>"
        sys.exit(0)

    alnfname = sys.argv[1]
    paramfname = sys.argv[2]

    alnfile = open(alnfname,"r")
    alignment = {}

    empty_partition = {}
    first = True
    for line in alnfile:
        if first:
            ntaxa, nsites = [int(n) for n in line.strip().split()]
            first = False
            continue

        try:
            name, seq = line.strip().split()
        except IndexError:
            continue

        alignment[name] = seq
        empty_partition[name] = []

    paramfile = open(paramfname,"r")
    pfilecontents = paramfile.readlines()

    site_assignments = [int(n) for n in pfilecontents[-1].strip().split("\t")]
    nparts = max(site_assignments)

    partitions = []
    for n in range(0,nparts+1):
        partitions.append(deepcopy(empty_partition))

    n = 0
    for site, p in enumerate(site_assignments):
        for name in alignment.iterkeys():
    #        print "site " + str(site) + " p " + str(p) + " name " + name
            partitions[p][name].append(alignment[name][site])
        n += 1
        if n % 1000 == 0:
            print "site " + str(n)

    alnoutfile = open(alnfname.rsplit(".phy",1)[0] + ".pb.part.alignment.phy","w")
    alnoutfile.write(str(ntaxa) + " " + str(nsites) + "\n")

    firstname = None
    for name in alignment.iterkeys():
        if firstname == None:
            firstname = name
    
        print name
        alnoutfile.write(name + " ")
        for part in partitions:
            alnoutfile.write("".join(part[name]))
        alnoutfile.write("\n")

    alnoutfile.close()

    partoutfile = open(alnfname.rsplit(".phy",1)[0] + ".pb.part.partitions.part","w")

    start = 1
    partnum = 0
    for part in partitions:
        partnum += 1
        partlen = len(part[firstname])
        if partlen == 0:
            continue

        end = start + partlen - 1
        partoutfile.write("DNA, " + str(partnum) + " = " + str(start) + "-" + str(end) + "\n")
        start = end + 1
 
    partoutfile.close()

    print nsites
