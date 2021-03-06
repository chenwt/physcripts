#!/usr/bin/env python

'''Subsample an alignment uniformly at random.'''

from phyaln import Alignment, SimpleSubsampler
    
if __name__ == '__main__':

    import argparse, copy, operator, os, random, re, sys 
    
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument('-a', '--alignment', type=open, required=True, \
        help='the location of the extended phylip alignment file to be subsampled.')
    
    parser.add_argument('-p', '--sampling-proportion', type=float, required=True, \
        help='a decimal value d | 0 < d < 1 to use as the sampling proportion. NOTE: no matter ' \
             'what value of d is provided, at least one sequence will be retained for every ' \
             'partition in the alignment.')
    
    parser.add_argument('-q', '--partitions', type=open, required=False, \
        help='the location of the raxml partitions file corresponding to the alignment to be subsampled.')
    
    parser.add_argument('-x', '--random-seed', type=int, required=False, \
        help='an integer seed for the random number generator function')
    
    parser.add_argument('-n', '--output-label', required=False, default='', \
        help='a label to be attached to output files')

    args = parser.parse_args()
    
    a = Alignment(args.alignment, args.partitions)
    s = SimpleSubsampler(a)
    
    random.seed()
    sampling_proportion = 0.5
    s.subsample(lambda: random.random() >= 0.5)

    s.write_subsampled_output(args.output_label)
    
    print('files have been written to: ' + s.output_label + '.sampling_matrix.txt, ' + s.output_label + '.subsampled.phy\n' \
              'sampling proportion is ' + str(s.get_sampling_proportion()))
