pp=python3

conference="cvpr"
topicnum=10
year=2021

if [ $# -gt 1 ]; then
year=$1
fi
mkdir $conference$year

$pp download_paper.py $year $conference
$pp pdftowordcloud.py $year $conference
$pp scrape_pdfs.py $year $conference
$pp makecorpus.py $year $conference
$pp genLDA.py $year $topicnum $conference
$pp genpages.py $year $topicnum $conference
