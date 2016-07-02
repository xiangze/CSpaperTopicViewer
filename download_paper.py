import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib2
import sys

year=2016
argc=len(sys.argv)
if(argc>1):
    year=int(sys.argv[1])

save_folder =str(year)

base_url = 'http://www.cv-foundation.org/openaccess/'

http = httplib2.Http()
status, response = http.request(base_url+'CVPR%d.py/'%year)

for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
        if link['href'] != "#" and link['href'].endswith('pdf'):
            file_url = link['href']
            start_index = file_url.rfind("/")+1
            filename = file_url[start_index:]

            pdf = urllib2.urlopen(base_url+file_url).read()
            with open(save_folder+filename, 'wb') as f:
                f.write(pdf)


