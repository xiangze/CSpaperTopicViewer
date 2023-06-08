pp=python3

conference="cvpr"
topicnum=10
year=2021

if [ $# -ge 1 ]; then
year=$1
fi
if [ $# -ge 2 ]; then
conference=$2
fi
echo $conference$year
mkdir -p $conference$year

# "cvpr"+"year" -> *.pdf
$pp download_paper.py $year $conference

# *.pdf -> topwords.p
$pp pdftowordcloud.py $year $conference

# *.pdf -> all_text.txt
$pp scrape_pdfs.py $year $conference

# *pdf -> alpapers.txt
$pp makecorpus.py $year $conference

for topicnum in 7 10 ;do
# allpapers.txt -> papers_%d.model'
    $pp genLDA.py $year $topicnum $conferenc
#dict:dictionary ,mm:corpus, papers_model:lda -> html
    $pp genpages.py $year $topicnum $conference
done
