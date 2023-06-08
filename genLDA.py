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

def makeLDAmodel(relpath,topicnum):
    rname= relpath+'/papers'
    print (relpath+"_"+str(topicnum))

    #if(not os.path.exists(rname+'.mm')):
    with open(relpath+'/allpapers.txt') as fp:
        d=fp.readlines()
        docs=[i.split(" ") for i in d]

    dictionary, corpus = prep_corpus(docs)

    MmCorpus.serialize(rname+'.mm',corpus)
    dictionary.save(rname+'.dict')

    t0=time.time()
    lda = models.ldamodel.LdaModel(corpus=corpus, 
                                id2word=dictionary,
                                num_topics=topicnum,
                                passes=10)

    print ("LDA Elapsed time %d"%(time.time()-t0))
                                        
    lda.save(relpath+'/papers_%d.model'%(topicnum))
   
def makeDTMmodel(conference,year_start,year_end,topicnum):
    docs=[]
    time_slices=[]
    for year in range(year_start,year_end+1):
        relpath=conference+str(year)
        rname= relpath+'/papers'    
        with open(relpath+'/allpapers.txt') as fp:
                d=[i.split(" ") for i in fp.readlines()]
        
        docs=docs+d
        time_slices.append(len(d))
    dictionary, corpus = prep_corpus(docs)

    t0=time.time()
    result  = models.LdaSeqModel(corpus,id2word=dictionary,
                                 time_slice=time_slices,
                                 num_topics=topicnum)
#    result  = models.LdaSeqModel(corpus,time_slices,topicnum)
 #   print ("DTM LDA Elapsed time %d"%time.time()-t0)
    result.save(conference+'_papers_%d.model'%(topicnum))
    result.print_topic()
    return result

if __name__ == "__main__":
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

    if(year==0):
        makeDTMmodel(conference,2016,2023,topicnum)
    else:
        makeLDAmodel(conference+str(year),topicnum)
    
