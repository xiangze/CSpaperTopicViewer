
# CVPR papers topic viewer

This is a set of scripts for creating visual summary for all papers published at CVPR. The original idea is from https://github.com/colincsl/cvpr2013papers
They show how one can manipulate PDFs, analyze word frequencies, 

#### Installation

0. Clone this repository `git clone https://github.com/xiangze/cvprpapers.git`

1. Make sure you have the following libraries [System: ghostscript, imagemagick; Python: httplib2, beautifulsoup]

```
pip3 install -r  requirements.txt
```

On OSX:
brew install ghostscript
brew install imagemagick
pip install httplib2
pip install beautifulsoup
pip install gensim
pip install pyLDAvis
pip install nltk

1.1 Download NLTK stopwords
```python
>>import nltk

>>nltk.download("stopwords")
```
 
 ```
 for year in `seq 2016 2023`;do
./run.sh cvpr $year
done
```
contents of run.sh

|python script|from|to|
|:----|:----|:----|
|download_paper.py|cvpr+"year"|$conference$year/*.pdf|
|pdftowordcloud.py|$conference$year/*.pdf|topwords.p|
|scrape_pdfs.py|$conference$year/*.pdf|all_text.txt|
|makecorpus.py|$conference$year/*.pdf|alpapers.txt|
|genLDA.py|allpapers.txt|papers_%d.model'|
|genpages.py|papers_model:lda|$conference$year_$topicnum.html|

#### Licence

WTFPL licence
