import gensim
import pyLDAvis
import pyLDAvis.gensim
import sys

year=2014
topic_num=10

argc=len(sys.argv)
if(argc>1):
    year=int(sys.argv[1])
if(argc>2):
    topic_num=int(sys.argv[2])

print  year, topic_num

fname='%d/CVPRpapers%d'%(year,year)

dictionary = gensim.corpora.Dictionary.load(fname+'.dict')
corpus = gensim.corpora.MmCorpus(fname+'.mm')
lda = gensim.models.ldamodel.LdaModel.load(fname+'_%d.model'%topic_num)

pdata=pyLDAvis.gensim.prepare(lda, corpus, dictionary)
p=pyLDAvis.prepared_data_to_html(pdata)

with open(fname+"_%d.html"%(topic_num),"w") as fp:
    print >>fp,"<h1> CVPR %d</h1>"%year
    print >>fp,"topic num=%d"%topic_num
    print >>fp,p
