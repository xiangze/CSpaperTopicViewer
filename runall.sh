conference="cvpr"
topicnum=10
year=2015

python download_paper.py $year $conference
python pdftowordcloud.py $year $conference
python scrape_pdfs.py $year $conference
python makecorpus.py $year $conference
python genLDA.py $year $topicnum $conference
python genpages.py $year $topicnum $conference
