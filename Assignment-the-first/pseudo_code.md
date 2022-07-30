# Assignment the First
## Part 2

**Pseudo code for Demultiplexing**

- open a dictionary for the index list. The keys will be the sequences and the values will be the reverse complement. 
- open a dictionary for the counts of records in each file. 
- open all the four input FASTQ, iterate over them at the same time and read record by record. 
- if the indexes are not in the indexes list or you have an N in the index, save the records in the "unknown" file. Add the indexes in the header. 
    - increment the dictionary with the records counts for the "unknown" file. 
- if index1 is equal to the reverse complement of index2, check to see if they are on the index list. 
    - if the indexes match and are on the indexes list:
        - quality scores filtering: if the quality scores of the index files are below the cutoff, save the records in the "unknown" file.
        - else: save the record of read1 and read2 in the "matched" file and include the index in the header and on the name of the file. Use the rev complement in the name, it is easy for others to see they match. 
            - increment the dictionary with the records counts for the "matched" file.
- if index1 and index2 are on the list, but they are not the reverse complement of each other, they are hopped. So, save the records in the "hopped" file (separated by reads). Also, include the indexes in the name of the file. No need to include it in the header.
    - increment the dictionary with the records counts for the "hopped" file.



