# Assignment the First

## Part 1
1. Be sure to upload your Python script.

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz | read1 | 101 | +33 |
| 1294_S1_L008_R2_001.fastq.gz | index1 | 8 | +33 |
| 1294_S1_L008_R3_001.fastq.gz | index2 | 8 | +33 |
| 1294_S1_L008_R4_001.fastq.gz | read2 | 101 | +33 |

2. i.Per-base NT distribution

**Read1**

![read1](https://user-images.githubusercontent.com/68506950/181681113-da9e4080-8ca0-433d-afa1-50ca72168ce2.png)


**Read2**


![read2](https://user-images.githubusercontent.com/68506950/181684308-0da662aa-87e5-4d8a-81b1-8507496e68dd.png)


**Index1**

![index1](https://user-images.githubusercontent.com/68506950/181684363-65044444-288e-4e20-bea3-eda998e39aab.png)


**Index2**

![index2](https://user-images.githubusercontent.com/68506950/181684382-56fab833-6185-4d46-b3ba-85799b108e86.png)


ii. What is a good quality score cutoff for index reads and biological read pairs to utilize for sample identification and downstream analysis, respectively? Justify your answer.

For the sample identification, it is necessary a higher Qscore cutoff, since we need our samples to be of higher quality in general. For that, I believe that a Q30 is a good quality score cutoff, with a base accuracy of >99.9%. The alignment process, that occurs later in the downstream analysis, can also filter for low-quality scores, so it is not necessary to have only high-quality reads. For that, I believe that a Q20 is a good cutoff, allowing a base accuracy of >99%.


iii. How many indexes have undetermined (N) base calls? (Utilize your command line tool knowledge. Submit the command(s) you used. CHALLENGE: use a one-line command)

zcat 1294_S1_L008_R2_001.fastq.gz | awk '(NR%4==2)' | grep -c "N"

3976613

zcat 1294_S1_L008_R3_001.fastq.gz | awk '(NR%4==2)' | grep -c "N"

3328051


## Part 2
1. Define the problem

Multiplexing is a strategy for sequencing different samples together. For the demultiplexing, we will use the barcode (indexes) information in order to know which sequences came from each sample. For that, we have a list of indexes, a file with the reads, and another one with the indexes for each read. For each of the records, it is necessary to see if they match with the indexes, if they are index-hopped or if they are unknown and save them in the appropriate output file.

2. Describe output

Because of the large number of output files expected, a table would be a good way to organize all of them.

3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement

- Reverse complement function:
```
def rev_comp(seq:str) -> str:
    ''' This function takes a sequence and returns the reverse complement.'''   
    pass
    return rc_seq
```
Test example:
```
Input: ATGCTA
Expected output: TAGCAT
````

- Phred score average:
```
def phred_score(letter:str) -> int:
    '''This funcion takes the quality score line in each record and returns the average'''
    pass
    return avg_phred
```
Test example:
```
Input: AAFFFJJJJJJJ
Expected output: 38
```
