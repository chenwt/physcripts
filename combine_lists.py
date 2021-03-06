#!/usr/bin/env python2.7

import os, sys, csv

if len(sys.argv) < 3:
    print("usage: combine_lists.py <input1> <input2> <keycolumn> [include=<col1,col2,...>] [exclude=<col1,col2,...>]")
    sys.exit(0)

key_column_label = sys.argv[3].strip()

# if the user has specified columns to include/exclude
colnames_to_include = set()
colnames_to_exclude = set()
user_include_colnames_set = False
user_exclude_colnames_set = False
if len(sys.argv) > 4:
    for arg in sys.argv[4:]:
        parts = arg.split("=")
        if parts[0] == "include":
            user_include_colnames_set = True
            for c in parts[1].split(","):
                colnames_to_include.add(c)
            print("will include: " + str(colnames_to_include))
        elif parts[0] == "exclude":
            user_exclude_colnames_set = True
            for c in parts[1].split(","):
                colnames_to_exclude.add(c)

recorded_colnames = set()

# read the first list
list1 = {}
list1_colnames = []
list1_key_column_index = -1
on_first_line = True
with open(sys.argv[1], "r") as list1_infile:

	list1_reader = csv.reader(list1_infile,delimiter=',',quotechar='"')
	for row in list1_reader:
		
		parts = [s.strip() for s in row]
		
		if list1_reader.line_num == 1:
			for i, val in enumerate(parts):
				if val == key_column_label:
					list1_key_column_index = i
					
			if list1_key_column_index == -1:
				print("the key column \"" + key_column_label + "\" must be present in both input lists") 
				sys.exit(0)

			list1_colnames = parts
			continue

		# make a new entry in the dict for this row
		key_value = parts[list1_key_column_index]
		list1[key_value] = {}

		# add all the other known values to the dict
		for i, val in enumerate(parts):
			if i != list1_key_column_index:
				list1[key_value][list1_colnames[i]] = val

list2 = {}
#>>>>>>> 0428333ff0d4a360f53d1d1c026a8301b4107398
list2_colnames = []
list2_key_column_index = -1
on_first_line = True
with open(sys.argv[2], "r") as list2_infile:

	list2_reader = csv.reader(list2_infile,delimiter=',',quotechar='"')
	for row in list2_reader:
				
		parts = [s.strip() for s in row]
		
		if list2_reader.line_num == 1:
			for i, val in enumerate(parts):
				if val == key_column_label:
					list2_key_column_index = i
					
			if list2_key_column_index == -1:
				print("the key column \"" + key_column_label + "\" must be present in both input lists") 
				sys.exit(0)

			list2_colnames = parts
			continue
			
		# make a new entry in the dict if we need one
		key_value = parts[list2_key_column_index]
		if key_value not in list1:
			print("adding a new row for " + key_value)
			list1[key_value] = {}

		# add all the other known values to the dict -- WILL OVERWRITE previously existing list values
		for i, val in enumerate(parts):
			if i != list2_key_column_index:
				list1[key_value][list2_colnames[i]] = val
#print list1
non_key_column_labels = list(set(list1_colnames + list2_colnames) - set([key_column_label,]))
non_key_column_labels.sort()
#recorded_colnames = list(recorded_colnames)
#print recorded_colnames
#recorded_colnames.sort()

print(",".join([key_column_label,] + list(non_key_column_labels)))
for key_value, other_columns in list1.items():
    other_values = []
    for v in non_key_column_labels:
#    for v in recorded_colnames:
        if v in other_columns:
            other_values.append("\""+other_columns[v]+"\"")
        else:
            other_values.append("\"\"")
    print(",".join([key_value,] + other_values))
