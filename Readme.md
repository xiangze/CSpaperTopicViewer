
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
 
2. Download CVPR papers using download_paper.py and put them into the folder papers/

3. Run `pdftowordcloud.py` (to generate top words for each paper. Output saved in topwords.p as pickle)

4. Run `scrape_cvpr.py` (to generate paperid, title, authors list by scraping html page)

5. Run `makecorpus.py` (to create allpapers.txt file that has all papers one per row)

6. Run `python genLDA.py $year $topicnum `. Model(*.model), dictionay file(*.dict), corpus(*.mm) are saved.

8. Finally, run `python genpages.py $year $topicnum` creates $year/CVPRpapers_$year_$k.html`

#### Licence

WTFPL licence
