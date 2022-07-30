#!/usr/bin/env python

import numpy as np
import gzip
import argparse
import bioinfo
import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser(description="A program to generate a per base distribution of quality scores")
    parser.add_argument("-f", "--filename", help="The name of the file you are using", type=str, required=True)
    parser.add_argument("-n", "--records_number", help="The number of records in the file", type=str, required=True)
    parser.add_argument("-l", "--length", help="The length of the reads", type=str, required=True)
    parser.add_argument("-o", "--output", help="The name of the output files", type=str, required=True)
    return parser.parse_args()

args = get_args()
f = args.filename
n = int(args.records_number)
l = int(args.length)
o = args.output

my_list=np.zeros(l)

a = 0
with gzip.open(f, "rt") as fh:
    i=0
    for line in fh:
        line=line.strip()
        i+=1
        if i % 4 == 0:
            #print(line)
            for ind, letter in enumerate(line): 
                    score=bioinfo.convert_phred(letter)
                    my_list[ind]+=score
            a+=1
#print(my_list)

mean=np.zeros(l)
for k in range(l):
    mean[k]=(my_list[k]/(i/4))
#print(mean)

plt.bar(np.arange(l), mean, color='purple')
plt.xlabel('Position')
plt.ylabel('Mean Qscores')
plt.title('Distribution of quality scores for each position')
#plt.show()
plt.savefig(o)