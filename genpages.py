import gensim
import pyLDAvis
import pyLDAvis.gensim
import sys

year=2016
topic_num=10

argc=len(sys.argv)
if(argc>1):
    year=int(sys.argv[1])
if(argc>2):
    topic_num=int(sys.argv[2])

if(argc>3):
    conference=sys.argv[3]

relpath= conference+str(year)
print (conference+str(year)+"_"+str(topic_num))

fname=relpath+'/papers'
outfname=relpath+'papers'

dictionary = gensim.corpora.Dictionary.load(fname+'.dict')
corpus = gensim.corpora.MmCorpus(fname+'.mm')
lda = gensim.models.ldamodel.LdaModel.load(fname+'_%d.model'%topic_num)

pdata=pyLDAvis.gensim.prepare(lda, corpus, dictionary)
p=pyLDAvis.prepared_data_to_html(pdata)

with open(outfname+"_%d.html"%(topic_num),"w") as fp:
    print >>fp,"<h1> %s %d</h1>"%(conference.upper(),year)
    print >>fp,"topic num=%d"%topic_num
    print >>fp,p
