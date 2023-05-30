# go over all pdfs in NIPS, get all the words from each, discard stop words,
# count frequencies of all words, retain top 100 for each PDF and dump a
# pickle of results into topwords.p

import os
from string import punctuation
from operator import itemgetter
import re
import _pickle as pickle
import sys

N= 100 # how many top words to retain

year=2016
conference="cvpr"

argc=len(sys.argv)
if(argc>1):
    year=int(sys.argv[1])

if(argc>2):
    conference=sys.argv[2]

if(argc>3):
    N=sys.argv[3]


# load in stopwords (i.e. boring words, these we will ignore)
stopwords = open("stopwords.txt", "r").read().split()
stopwords = [x.strip(punctuation) for x in stopwords if len(x)>2]

# get list of all PDFs supplied by NIPS
relpath = conference+str(year)

allFiles = os.listdir(relpath)
pdfs = [x for x in allFiles if x.endswith(".pdf")]

# go over every PDF, use pdftotext to get all words, discard boring ones, and count frequencies
topdict = {} # dict of paperid -> [(word, frequency),...]
for i,f in enumerate(pdfs):
	# paperid = f[9:-4]
	paperid = f
	fullpath = relpath + "/"+f

	print("processing %s, %d/%d" % (paperid, i, len(pdfs)))

	# create text file
	cmd = "pdftotext %s %s" % (fullpath, "out.txt")
	print ("EXEC: " + cmd)
	os.system(cmd)

	txtlst = open("out.txt").read().split() # get all words in a giant list
	words = [x.lower() for x in txtlst if re.match('^[\w-]+$', x) is not None] # take only alphanumerics
	words = [x for x in words if len(x)>2 and (not x in stopwords)] # remove stop words

	# count up frequencies of all words
	wcount = {}
	for w in words: wcount[w] = wcount.get(w, 0) + 1
	top = sorted(wcount.items(), key=itemgetter(1), reverse=True)[:N] # sort and take top N

	topdict[paperid] = top # save to our dict

# dump to pickle
pickle.dump(topdict, open("topwords.p", "wb"))
