from glob import glob
from gensim import models
from gensim.corpora import Dictionary, MmCorpus
import nltk
import sys
import os
import time

def nltk_stopwords():
    return set(nltk.corpus.stopwords.words('english'))

def prep_corpus(docs, additional_stopwords=set(), no_below=5, no_above=0.5):
  print('Building dictionary...')
  dictionary = Dictionary(docs)
  stopwords = nltk_stopwords().union(additional_stopwords)
  stopword_ids = map(dictionary.token2id.get, stopwords)
  dictionary.filter_tokens(stopword_ids)
  dictionary.compactify()
  dictionary.filter_extremes(no_below=no_below, no_above=no_above, keep_n=None)
  dictionary.compactify()

  print('Building corpus...')
  corpus = [dictionary.doc2bow(doc) for doc in docs]

  return dictionary, corpus

import sys
year=2016
conference="cvpr"

argc=len(sys.argv)
if(argc>1):
    year=int(sys.argv[1])

if(argc>2):
    topicnum=int(sys.argv[2])

if(argc>3):
    conference=sys.argv[3]

relpath= conference+str(year)
rname= relpath+'/papers'
print  conference,year, topicnum

if(not os.path.exists(rname+'.mm')):
    with open(relpath+'/allpapers.txt') as fp:
        d=fp.readlines()
        docs=[i.split(" ") for i in d]

        dictionary, corpus = prep_corpus(docs)

        MmCorpus.serialize(rname+'.mm',
                           corpus)
        dictionary.save(rname+'.dict')

t0=time.clock()
lda = models.ldamodel.LdaModel(corpus=corpus, 
                               id2word=dictionary,
                               num_topics=topicnum,
                               passes=10)
print time.clock()-t0
                                      
lda.save(relpath+'/papers_%d.model'%(topicnum))

