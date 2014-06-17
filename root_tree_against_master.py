#!/usr/bin/env python

import sys, newick3, phylo3

def get_bipart(node):

	if node.parent == None:
		bipart = (set([l.label for l in set(node.children[0].leaves())]), \
				  set([l.label for l in set(node.children[1].leaves())]))
	else:
		ingroup = get_labels(node.leaves())
		parent = node
		while parent.parent != None:
			parent = parent.parent
		bipart = (ingroup, get_labels(parent.leaves()) - ingroup)
	
	assert(len(bipart[0]) > 0)
	assert(len(bipart[1]) > 0)
	
	return bipart

def get_string(bipart):
	return get_string_partial(bipart[0]) + " | " + get_string_partial(bipart[1])

def get_string_partial(labels):
	return "[" + (", ".join(labels) if len(labels) > 0 else "") + "]"

def get_labels(nodeset):
	return set([(l.label if l.label != None else "") for l in nodeset]) if nodeset != None else []
	
def is_compatible(bipart0, bipart1):
	if (len(bipart0[0].intersection(bipart1[0])) > 0 and len(bipart1[1].intersection(bipart0[0])) == 0 and \
	   	len(bipart0[1].intersection(bipart1[1])) > 0 and len(bipart1[0].intersection(bipart0[1])) == 0) or \
	   (len(bipart0[0].intersection(bipart1[1])) > 0 and len(bipart1[0].intersection(bipart0[0])) == 0 and \
		len(bipart0[1].intersection(bipart1[0])) > 0 and len(bipart1[1].intersection(bipart0[1])) == 0):
	   	return True
	else:
		return False

if __name__ == "__main__":
	if len(sys.argv) < 3:
		sys.exit("usage: root_tree_against_master.py <treetoroot> <mastertree>")

	with open(sys.argv[1], "r") as target_file:
		target = newick3.parse(target_file)
	if len(target.leaves()) < 3:
		sys.exit("cannot perform rooting on a tree with fewer than three tips")

	with open(sys.argv[2], "r") as master_file:
		master = newick3.parse(master_file)
	if len(master.leaves()) < 3:
		sys.exit("cannot perform rooting against a master tree with fewer than three tips")

	labels_missing_from_master = get_labels(target.leaves()).difference(get_labels(master.leaves()))
	if len(labels_missing_from_master) > 0:
		sys.exit("the labels " + ", ".join(labels_missing_from_master) + \
				 " are missing from the master tree, making unambiguous rooting impossible.")

	# get the mrca from the master tree of all the tips in the target
	master_mrca = phylo3.get_mrca(master, [l.label for l in target.leaves()])
	
	if len(master_mrca.children) != 2:
		sys.exit("mrca in master tree must define a biparition, not a multifurcation!")
		
	# get the bipart *below* the master mrca, since all target taxa are contained by it
	master_bipart = get_bipart(master_mrca.children[0])

	# first check if the current root is already compatible
	if is_compatible(get_bipart(target), master_bipart):
		print(newick3.to_string(target)+";\n")
		sys.exit("already rooted correctly! just reiterated original topology.")

	for test_root in target.descendants():
		test_bipart = get_bipart(test_root)
		if is_compatible(test_bipart, master_bipart):
#			print("found node in input tree compatible with root node in master: " + get_string(test_bipart))
#			print("old topology is: " + newick3.to_string(test_root))
			rooted_tree = phylo3.get_tree_rooted_on(test_root)
			print(newick3.to_string(rooted_tree)+";\n")
			break