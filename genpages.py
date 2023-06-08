import gensim
from gensim.models import LdaModel, CoherenceModel
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import sys
import genLDA as gl
import os

def genpages(relpath,topic_num,writemode="w",outfname=""):
    fname=relpath+'/papers'

    if(writemode!="a"):
        outfname=relpath+"papers_%d.html"%(topic_num)

    dictionary = gensim.corpora.Dictionary.load(fname+'.dict')
    corpus = gensim.corpora.MmCorpus(fname+'.mm')
    lda = gensim.models.ldamodel.LdaModel.load(fname+'_%d.model'%topic_num)

    perplexity = 2**(-lda.log_perplexity(corpus))
    cm= CoherenceModel(model = lda, corpus = corpus, coherence = 'u_mass')
    coherence = cm.get_coherence()

    pdata=gensimvis.prepare(lda, corpus, dictionary)
    p=pyLDAvis.prepared_data_to_html(pdata)

    print("relpath "+relpath)
    print("topic num=%d"%topic_num)
    print("perplexity =%g"%perplexity)
    print("coherence =%g"%coherence)
    
    with open(outfname,writemode) as fp:
        fp.writelines("<h1> %s %d</h1>"%(conference.upper(),year))
        fp.writelines("topic num=%d,"%topic_num)
        fp.writelines("perplexity =%g,"%perplexity)
        fp.writelines("coherence =%g,"%coherence)
        fp.writelines(p)
        
    return perplexity,coherence

def genperp(relpath,topic_num):
    fname=relpath+'/papers'

    corpus = gensim.corpora.MmCorpus(fname+'.mm')
    
    LDAfilename=fname+'_%d.model'%topic_num
    if(not os.path.exists(LDAfilename)):
        gl.makeLDAmodel(relpath,topic_num)
    lda = gensim.models.ldamodel.LdaModel.load(LDAfilename)    
        
    perplexity = 2**(-lda.log_perplexity(corpus))
    cm= CoherenceModel(model = lda, corpus = corpus, coherence = 'u_mass')
    coherence = cm.get_coherence()
    return perplexity,coherence

if  __name__ == "__main__":
    year=2016
    topic_num=10
    year_end=2016

    argc=len(sys.argv)
    if(argc>1):
        year=int(sys.argv[1])
    if(argc>2):
        topic_num=int(sys.argv[2])

    if(argc>3):
        conference=sys.argv[3]

    if(argc>4):
        year_end=int(sys.argv[4])
        
    if(year==year_end):
        genpages(conference+str(year),topic_num)
    elif(topic_num==0):        
    #perplexity of various
        pps=[]
        for topic_num in range(4,16):
                relpath=conference+str(year)
                perplexity,coherence=genperp(relpath,topic_num)
                pps.append([topic_num,perplexity,coherence])

        with open("perp_%s%d.csv"%(conference,year),"w") as fp:
                fp.writelines("topicnum,perplexity,coherence\n")
                for topic_num,perplexity,coherence in pps:
                    fp.writelines("%d,%g,%g\n"%(topic_num,perplexity,coherence))
    else:        
    #multiple years
        for y in range(year,year_end+1):
                relpath=conference+str(year)
                gl.makeLDAmodel(relpath,topic_num)
                perplexity,coherence=genpages(relpath,topic_num,"a",conference+"papers_%d.html"%(topic_num))
                
