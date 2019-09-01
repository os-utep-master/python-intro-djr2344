# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 21:23:58 2019

@author: Derek

Sources Cited:
    method for removing non-alphanumeric characters (lines 20 -> 22):
        <https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python>

"""

import sys        # command line arguments
import re         # regular expression tools
import os         # checking if file exists
import subprocess # executing program
import string
from sys import exit

def ExtractAlphanumeric(InputString):
    from string import ascii_letters, digits
    return "".join([ch for ch in InputString if ch in (ascii_letters + digits + ' ')])

# set input and output files
if len(sys.argv) is not 3:
    print("Correct usage: <input text file> <output file>")
    for argg in sys.argv:
            print(argg)
    sys.exit()
for argg in sys.argv:
            print(argg)    

textFname = sys.argv[1]
outputFname = sys.argv[2]

#make sure text files exist
if not os.path.exists(textFname):
    print ("text file input %s doesn't exist! Exiting" % textFname)
    sys.exit()
    
#make sure output file exists
if not os.path.exists(outputFname):
    print ("wordCount output file %s doesn't exist! Exiting" % outputFname)
    sys.exit()
 
# attempt to open input file
with open(textFname, 'r') as inputFile:
    wordlist = []
    full_tx = ""
    for line in inputFile:
        # get rid of newline characters
        line = line.strip()
        newline = ""
        #get rid of non-alpha chars
        newline = ExtractAlphanumeric(line)
        #compile lines to single string
        full_tx = full_tx + " " + newline
    #split string for list of words
    word_list = re.split('[ \t]', full_tx.lower())

wordfreq = []
wordfreq = [str(word_list.count(w)) for w in word_list] #get word counts
results = set( zip(word_list, wordfreq) ) #create the sets of (word, word-count)
s_results = sorted(results,key= lambda x: x[0]) #sort set for descending order

empt = 0
with open(outputFname, 'w') as outputFile:
    for r in s_results:
        if (empt != 0):  #skip first set that references junk
            ent = ""
            ent = str(r[0]) + " " + str(r[1])
            outputFile.write(str(ent)) #write line to output file
            outputFile.write('\n')
        empt = empt + 1
    
sys.exit()
