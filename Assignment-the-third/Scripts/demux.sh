#!/bin/bash

#SBATCH --partition=bgmp        ### Partition (like a queue in PBS)
#SBATCH --job-name=demux      ### Job Name
#SBATCH --output=demux%j.out         ### File in which to store job output
#SBATCH --error=Hi_demux%j.err          ### File in which to store job error messages
#SBATCH --time=0-10:00:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --nodes=1               ### Number of nodes needed for the job
#SBATCH --cpus-per-task=1     ### Number of tasks to be launched per Node
#SBATCH --account=bgmp      ### Account used for job submission

# ./demultiplex.py                         # run your actual program

r1="/../../../projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz"
i1="/../../../projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz"
i2="/../../../projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz"
r2="/../../../projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz"
indexes="/../../../projects/bgmp/shared/2017_sequencing/indexes.txt"

/usr/bin/time -v ./demultiplex.py \
    -f1 $r1 -f2 $r2 -i1 $i1 -i2 $i2 \
    -ind $indexes \
    -c 30 
echo "DONE"

