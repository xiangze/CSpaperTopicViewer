import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request, urllib.error
import os
import re
import sys

def get(url):
    http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
    status, response = http.request(url)
    return response

def getlinks(url):
     return BeautifulSoup(get(url),"html.parser", parse_only=SoupStrainer('a'))

def pdfname(file_url,save_folder):
     start_index = file_url.rfind("/")+1
     return save_folder+"/"+file_url[start_index:]

def savepdf(link,base_url,save_folder):
    if link != "#" and link.endswith('pdf'):
        outfilename=pdfname(link,save_folder)
        if(not os.path.exists(outfilename)):
            pdf = urllib.request.urlopen(base_url+link).read()
            with open(outfilename, 'wb') as f:
                f.write(pdf)


def download_papers(conference,year,save_folder):
    if(not os.path.exists(save_folder)):
        os.mkdir(save_folder)


    if(conference=="cvpr"):
        base_url = 'https://openaccess.thecvf.com/'
        if(year>= 2018 and year <= 2020):
            links_days=[ base_url+a.get("href") for a in getlinks(base_url+'CVPR%d'%year) ]

    #        print(links_days) 
    #        exit()

            for l in links_days:
                #print(getlinks(l))
                for link in getlinks(l):
                    if link.has_attr('href'):
                        try:
                            savepdf(link['href'],base_url,save_folder)
                        except:
                            print("no PDF file: %s  !!!"%link.text)
        else:
            url=base_url+'CVPR%d?day=all'%year
            links=getlinks(url)
            for link in links:
                if link.has_attr('href'):
                    try:
                        savepdf(link['href'],base_url,save_folder)
                    except:
                        print("no PDF file: %s  !!!"%link.text)

    elif(conference=="iccv"):
        base_url = 'https://openaccess.thecvf.com/'
        links=getlinks(base_url+'ICCV%d'%year)
        for link in links:
            if link.has_attr('href'):
                savepdf(link['href'],base_url,save_folder)

    elif(conference=="nips"):
        base_url = 'https://papers.nips.cc/'
        links=getlinks(base_url)
        for l in links:
            if(len(re.findall(str(year),l.text))>0):
                turl=l['href']

        links_of_year=getlinks(base_url+turl)
        print( len(links_of_year))

        for l in links_of_year:
            links_of_a_paper=getlinks(base_url+l['href'])
            for link in links_of_a_paper:
                if link.has_attr('href'):
                    savepdf(link['href'],base_url,save_folder)

    else:
        print("not supperted conference :%s"%conference)

if __name__ == "__main__":
    year=2016
    conference="cvpr"

    argc=len(sys.argv)
    if(argc>1):
        year=int(sys.argv[1])

    if(argc>2):
        conference=sys.argv[2]

    download_papers(conference,year,
                    save_folder=conference+str(year))
