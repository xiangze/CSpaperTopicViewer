import sys
import glob
import PyPDF2
from PyPDF2 import PdfFileReader
from PyPDF2.pdf import ContentStream
from IPython import embed

def get_text(page):

	content = page['/Contents'].getObject()
	content = ContentStream(content, page.pdf)

	text = u""
	for operands,operator in content.operations:
		if operator in ["TJ", "Tj"]:
			for i in operands[0]:
				if isinstance(i, PyPDF2.generic.TextStringObject):
					if type(text) is not list:
						text += i
				elif type(i) is PyPDF2.generic.NumberObject and i < 0:
					text += " "
		elif operator in ['Tf']:
			text += " "

	remove = [u"\u201d", u"\u201c"]
	for r in remove:
		text = text.replace(r, u" ")
	text = text.replace(u"\ufb01", u"fi")

	return text

def scrape_pdfs(folder):
        #files = [x for x in os.listdir(folder) if x[-3:]=='pdf']
        files = glob.glob(folder+"/*.pdf")
        text_out = open(folder+'all_text.txt', 'w')

        titles = []
        authors = []
        keywords = []
        body = []

        for i,f in enumerate(files):
	        reader = PdfFileReader(open(f, 'rb'))
	        info = dict(reader.documentInfo)
                #	titles += [info['/Title']]
                #	authors += [info['/Author']]
                #	keywords += [info['/Keywords']]

	        content = ""
	        for p in range(reader.numPages):
		        page = reader.getPage(p)
		        content += get_text(page)

			body += [content]

        for b in body:
	        text_out.write(b.encode("ascii", "ignore"))
                # for t in titles:
	        # text_out.write(t+"\n-\n\n")
        text_out.close()


if  __name__ == "__main__":
        year=2016
        conference="cvpr"

        argc=len(sys.argv)
        if(argc>1):
                year=int(sys.argv[1])

        if(argc>2):
                conference=sys.argv[2]
    
        scrape_pdfs(conference+str(year))
