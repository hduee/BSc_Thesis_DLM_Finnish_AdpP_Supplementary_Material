############ This script prints out comma-separated spreadsheet(s) (report-language.csv) with the ratio of word order pairs in conllu files ########
#!/usr/bin/env python3
import sys
import subprocess
import re
import pprint
import glob
import os
import random
import unicodedata
import collections
import csv
import string
import io
import conllu
from bs4 import BeautifulSoup
from pathlib import Path

try:
    import argparse
except ImportError:
    checkpkg.check(['python-argparse'])

import time
import socket

"""

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

USAGE = './ud-length.py -s <vrt_file>'

def build_parser():

    parser = argparse.ArgumentParser(description='ud-length: Extract sentence length')
    parser.add_argument('-s', '--source', required=True, help='Source for vrt files')
    parser.add_argument('-t', '--target', required=True, help='target for report files')
    parser.add_argument('-l', '--length', type=int, required=False, help='most common length')

    return parser


def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}

def udlength(conllufile):
    from conllu import parse
    length = list()
    data = open(conllufile, mode="r", encoding="utf-8")
    soup = BeautifulSoup(data)
    for text in soup.children:
        for s in text.children:
            for tokens in (parse(s.text)):
                length.append(len(tokens))
    return max(set(length), key=length.count)

def udsurplength(conllufile,length,report):
    from conllu import parse
    data = open(conllufile, mode="r", encoding="utf-8")
    soup = BeautifulSoup(data)
    lang = Path(conllufile).stem.split("_")[0]
    for children in soup.children:
        for body in children:
            for text in body:
                for s in text:
                    for sentence in s:
                        for tokens in (parse(sentence,fields=["id", "form", "lemma", "upos", "xpos", "feats", "head", "deprel", "deps", "misc", "surprise"])):
                            print("Analyzing sentence "+tokens.metadata['sent_id'])
                            if len(tokens) == length:
                                row = list()
                                row.append(lang)
                                row.append(text.attrs['id']+"-"+text.attrs['language']+"-"+tokens.metadata['sent_id'])
                                for token in tokens:
                                    row.append(token['surprise'])
                                report.writerow(row)
    return



def main():
    global debug
    global args
    global seppath
    global synroles
    parser = build_parser()
    args = parser.parse_args()
    '''Check arguments'''    
    if check_args(args) is False:
     sys.stderr.write("There was a problem validating the arguments supplied. Please check your input and try again. Exiting...\n")
     sys.exit(1)
    '''Unknown function, I'll check it later''' 
    start_time = time.time()
    length = dict()
    if args.length == None:
        for conllufile in sorted(glob.glob(args.source+'/*.vrt')):
            print("Searching for the most commont sentence length...")
            length[os.path.basename(conllufile).split("_")[0]] = udlength(conllufile)
            print("Done with "+conllufile)
        values_list = list(length.values())
        common_length = max(set(values_list), key=values_list.count)
    else:
        common_length = args.length
    print("Most common length is "+str(common_length))
    for conllufile in sorted(glob.glob(args.source+'/*.vrt')):
        csvfile = open(args.target+"report-"+Path(conllufile).stem.split("_")[0]+".csv", 'a+', newline='',encoding='utf-8')
        report = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        length = common_length
        print("Analyzing sentences with length = "+str(common_length))
        header = list()
        while (common_length > 0):
            header.append(common_length)
            common_length -= 1
        header.sort()
        header.insert(0,"sent")
        header.insert(0,"lang")
        report.writerow(header)
        udsurplength(conllufile,length,report)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("Done! Happy corpus-based typological linguistics!\n")

if __name__ == "__main__":
    main()
    sys.exit(0)

