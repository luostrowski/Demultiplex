#!/usr/bin/env python
import gzip
import bioinfo
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="A program to demultiplex your samples")
    parser.add_argument("-f1", "--filename1", help="The name of the file with your biological reads", type=str, required=True)
    parser.add_argument("-f2", "--filename2", help="The name of the file with your biological reads (if dual-matched)", type=str, required=False)
    parser.add_argument("-i1", "--filename3", help="The name of the file with your index reads", type=str, required=True)
    parser.add_argument("-i2", "--filename4", help="The name of the file with your index reads (if dual-matched)", type=str, required=False)
    parser.add_argument("-ind", "--file_index", help="The name of the file with your indexes list", type=str, required=True)
    parser.add_argument("-c", "--cutoff", help="The cutoff for quality score", type=int, required=True)
    return parser.parse_args()

args = get_args()
f1 = args.filename1
f2 = args.filename2
i1 = args.filename3
i2 = args.filename4
ind = args.file_index
c = args.cutoff

complement={"A":"T", "C":"G", "G":"C", "T":"A", "N":"N"}
def rev_comp(seq:str) -> str:
    ''' This function takes a sequence and returns the reverse complement.'''   
     ##if the index has a N also needs to be reversed complemented
    new_seq=""
    for base in seq:
        new_seq+=complement[base]
    return new_seq[::-1]

indexes={} ## dict for the indexes; keys are the indexes and values will be the two file handles
#rev_comp_ind=()

with open(ind, "r") as fq:
    fq.readline() ##read the header but do not interact with it
    for line in fq:
        line=line.split("\t")
        idx = line[4].strip("\n")##selecting for the forth line
        indexes[idx] = [open(f"out/{idx}_R1.fq", "w"), open(f"out/{idx}_R2.fq", "w")]
    #print(indexes)

hopped1_fh = open("out/hopped_R1.fq", "w") ##opening files for hopped reads
hopped2_fh = open("out/hopped_R2.fq", "w")
unknown1_fh = open("out/unknown_R1.fq", "w") ##opening files for unknown reads
unknown2_fh = open("out/unknown_R2.fq", "w")

i=0 #lines counter
record1_list=[]
record2_list=[]
index1list_=[]
index2_list=[]
count_hopped=0
count_unknown=0
count_matched=0
below_qscore=0
idx_counts={}
##opening four files at the same time
with gzip.open(f1, "rt") as read1, gzip.open(f2, "rt") as read2, gzip.open(i1, "rt") as index1, gzip.open (i2, "rt") as index2:
    while True: ##selecting only the first four lines
        i+=4
        record1_list=[read1.readline().strip(),read1.readline().strip(),read1.readline().strip(),read1.readline().strip()] ##each record have four lines
        record2_list=[read2.readline().strip(),read2.readline().strip(),read2.readline().strip(),read2.readline().strip()]
        index1_list=[index1.readline().strip(),index1.readline().strip(),index1.readline().strip(),index1.readline().strip()]
        index2_list=[index2.readline().strip(),index2.readline().strip(),index2.readline().strip(),index2.readline().strip()]
        #print(record1_list)
        if record1_list[0]=="": ##break when we reach the end of the file (all the files have the same length)
            break
        revcomp2 = rev_comp(index2_list[1]) ##saving rev comp of index 2 in variable
        idx_pair = index1_list[1] +"-"+revcomp2 ##defining a string with the index-pair
        record1_list[0] += ":"+ idx_pair ##concatenating indexes in the header (keeping what is already there)
        record2_list[0] += ":"+ idx_pair
        record1_str='\n'.join(record1_list) ##transforming list in string separated by lines
        record2_str='\n'.join(record2_list)
        if index1_list[1] not in indexes or revcomp2 not in indexes: ##checking if indexes are not in the dict keys
            # note that our indexes do not contain N so those are saved to unknown by default
            print(record1_str, file=unknown1_fh)
            print(record2_str, file=unknown2_fh)
            count_unknown+=1 ##incrementing counter for total of read-pairs unknown
        else:  ##if the indexes are on the list
            if index1_list[1] != revcomp2: ##checking if index is different than rev comp
                print(record1_str, file=hopped1_fh)
                print(record2_str, file=hopped2_fh)
                count_hopped+=1 #incrementing counter for total of read-pairs hopped
                if idx_pair not in idx_counts:
                    idx_counts[idx_pair]=1
                else:
                    idx_counts[idx_pair]+=1
            else:
                if bioinfo.qual_score(record1_list[3]) < c or bioinfo.qual_score(record1_list[3]) < c: ##getting rid of reads with quality below cutoff
                    print(record1_str, file=unknown1_fh)
                    print(record2_str, file=unknown2_fh)
                    below_qscore+=1
                else:
                    print(record1_str, file=indexes[index1_list[1]][0]) ##changing the name of the key for the index and calling the first file handle in the dict values
                    print(record2_str, file=indexes[index1_list[1]][1]) ##changing the name of the key for the index and calling the second file handle in the dict values
                    count_matched+=1 #incrementing counter for total of read-pairs matched
                    if idx_pair not in idx_counts:
                        idx_counts[idx_pair]=1
                    else:
                        idx_counts[idx_pair]+=1

for key, (fh1, fh2) in indexes.items(): ##concatening files to close together
    fh1.close()
    fh2.close()

##closing files
hopped1_fh.close()
hopped2_fh.close()
unknown1_fh.close()
unknown2_fh.close()

total_reads = (count_hopped+count_matched+count_unknown+below_qscore)
total_matched = (count_matched+below_qscore)
print("Total number of reads:", total_reads)
print("Unknown reads-pairs:", count_unknown)
print("Percentage of read-pairs unknown:", round((count_unknown/total_reads)*100, 2),"%")
print("Hopped reads-pairs:", count_hopped)
print("Percentage of read-pairs hopped:", round((count_hopped/total_reads)*100, 2),"%")
print("Total matched reads-pairs:", total_matched)
print("Matched reads-pairs:", count_matched)
print("Percentage of read-pairs matched:", round((count_matched/total_reads)*100, 2),"%")
print("Reads with quality score below cutoff:", below_qscore)
print("Percentage of matched reads below qscore:", round((below_qscore/total_matched)*100, 2), "%")

new_file=open("indexes_counts.tsv", "w")
for k,v in idx_counts.items():
    print(f"{k}\t{v}", file=new_file)
new_file.close()