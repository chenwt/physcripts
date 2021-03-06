#!/usr/bin/env python
"""transpose_fastas.py
version 0.1
cody hinchliff
2012.7.21

This script accesses a directory, and traverses all FASTA files in it, recording them into a dict object. It then
writes new fasta files to a directory named 'inverted' within the provided dir. One inverted fasta file is created
for each sequence id found in the original set of fastas; each of these files contains the sequences associated
with this sequence id, labeled with ids representing the original fasta files whence they came.
	
For example, if the script is passed a directory containing fasta files corresponding to loci, containing sequences
labeled with taxon names, the inverted directory will contain fasta files corresponding to taxon names, containing
sequences labeled with locus names (drawn from the filenames of the original fastas)."""

if __name__ == "__main__":
    
    import sys
    import os
    
    # if called for a target outside the cwd, get a path to the target dir
    cwd = os.getcwd() + os.sep
    try:
        specdir = sys.argv[1]
        if specdir[0] == '/':
            dirpath = specdir
        else:
            dirpath = cwd + specdir
    except IndexError:
            print "No target directory specified, using current working directory."
            dirpath = ""

    if dirpath[-1] != "/":
            dirpath += "/"

    print "Reading files from: " + dirpath

    # attempt to get a list of files
    try:
        infiles = os.listdir(dirpath)
    except OSError:
        exit("There was a problem opening the specified directory. Are you sure it exists?")

    # the data dict will hold all the sequences in a indexed structure
    data = dict()

    # the seqids list will store all the sequence ids we find, which will be used to name the inverted files 
    seqids = list()

    # walk the list of input files (assumes all non-system files are fastas!)
    for infname in infiles:
            if infname in ("") or infname[0] == "." or os.path.isdir(infname):
                    continue

            # attempt to determine a useful filename id for this input file
            infile = file(dirpath + infname, 'rU')
            infid = os.path.basename(infile.name).rsplit(".fasta")[0].rsplit(".fst")[0]
            print infile.name

            # create a container to hold this file's sequences
            data[infid] = dict()

            # gather sequences from this file
            curseqid = ""
            for line in infile:
                    lineclean = line.strip()

                    if len(lineclean) == 0:
                            continue

                    # if we hit a sequence identifier line, record it, create a new sequence element
                    if lineclean[0] == ">":
                            curseqid = lineclean.strip(">")
                            seqids.append(curseqid)
                            data[infid][curseqid] = ""

                    # otherwise this line contains sequence data; add it to the current sequence element
                    else:
                            data[infid][curseqid] += lineclean

    # uniquify the list of seqids
    seqids = list(set(seqids))
    seqids.sort()

    try:
            os.mkdir(dirpath + "inverted")
    except OSError:
            pass

    # for each unique seq id
    for seqid in seqids:

            # create a file to contain the corresponding seqs out of the original alignments
            outfname = dirpath + "inverted/" + seqid + ".fasta"
            outfile = file(outfname, "w")

            # look through input data for seqs matching this seqid
            for infname, infdata in data.iteritems():

                    # write each matching sequence into the outfile, labeled with the name of the file whence it came
                    try:
                            seq = infdata[seqid]
                            outfile.write(">" + infname + "\n") 
                            outfile.write(seq + "\n")

                    # this file didn't contain a sequence with this id, so move on
                    except KeyError:
                            pass

    exit("\nTranposed fasta files have been written to:\n%s" % dirpath + "inverted")
