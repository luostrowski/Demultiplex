#!/usr/bin/env python
# Author: Luiza H. Ostrowski (ostrowski.luiza@gmail.com)

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "0.4"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = set('ATGCNatcgn')
RNA_bases = set('AUGCNaucgn')

def convert_phred(letter: str) -> int:
    """Converts a single character into a phred score"""
    return ord(letter) - 33

if __name__ == "__main__":
    """Check that convert_phred returns the correct value for several different inputs"""
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")

def qual_score(phred_score: str) -> float:
    """Calculate the average quality score of the phred string"""
    s = 0 #sum of scores
    l = 0 #number of letters
    for letter in phred_score:
        s+=convert_phred(letter)
        l+=1
    return s/l

def validate_base_seq(seq:str,RNAflag:bool=False) -> bool:
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    seq=seq.upper()
    return len(seq) == seq.count("A") + seq.count("U" if RNAflag else "T") + seq.count("G") + seq.count("C")

if __name__ == "__main__":
    assert validate_base_seq("AATAGAT") == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True) == True, "Validate base seq does not work on RNA"
    print("Passed DNA and RNA tests")

def gc_content(DNA):
    '''Returns GC content of a DNA sequence as a decimal between 0 and 1.'''
    DNA = DNA.upper()         #Make sure sequence is all uppercase
    Gs = DNA.count("G")       #count the number of Gs
    Cs = DNA.count("C")       #count the number of Cs
    return (Gs+Cs)/len(DNA)

if __name__ == "__main__":
    assert gc_content("GCGCGC") == 1, "messed up calc when all GC"
    assert gc_content("AATTATA") == 0
    assert gc_content("GCATGCAT") == 0.5
    print("correctly calculated GC content")

def oneline_fasta(file: str, new_file: str):
    '''This function takes a fasta file with multiple sequence lines and combine them together.'''
    seq=""
    header = ""
    new_fh = open(new_file, "w")
    with open(file, "r") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(">"):
                if seq != "":
                    print(f"{header}\n{seq}", file=new_fh)
                header = line
                seq = "" ##restart protein at each new record
            else:
                seq+=line
    print(f"{header}\n{seq}", file=new_fh)
    new_fh.close()
    return None


def populate_list(file: str) -> tuple[list, int]:
    """This function creates a list with the sum of the converted quality scores for each base pair."""
    score_list = []
    score_list = init_list(score_list)
    with open(file, "r") as fh:
        i=0
        for line in fh:
            line=line.strip()
            i+=1
            if i % 4 == 0:
                for ind, letter in enumerate(line): 
                    score=bioinfo.convert_phred(letter)
                    score_list[ind]+=score
    return score_list, i

def get_median (lst: list) -> float:
    """This function sort a list and returns the median value."""
    sorted_list=sorted(lst)
    mid=len(sorted_list)//2
    if len(sorted_list) % 2 != 0:
        md = sorted_list[mid]
    else:
        md = (sorted_list[mid] + sorted_list[(mid-1)]) / 2
    return md