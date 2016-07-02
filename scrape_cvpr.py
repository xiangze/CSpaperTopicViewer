# scrape the CVPR PDFs file looking for authors names, titles
# and create a database of all papers. This is necessary because
# extracting the authors and titles from PDFs directly is tricky.

import pyPdf
from pyPdf import PdfFileReader
import os
import cPickle as pickle
import random

papers_dir = 'papers/'

class Paper:
	def __init__(self, id_=None, title=None, authors=None, filename=None, keywords=None):
		self.paper = id_ # the id of the paper
		self.title = title # the title of the paper
		self.authors = authors # the author list of the paper
		self.filename = filename
		self.keywords = keywords


def get_text(page):

	content = page['/Contents'].getObject()
	content = pyPdf.pdf.ContentStream(content, page.pdf)

	text = u""
	for operands,operator in content.operations:
		if operator in ["TJ", "Tj"]:
			for i in operands[0]:
				if isinstance(i, pyPdf.generic.TextStringObject):
					if type(text) is not list:
						text += i
				elif type(i) is pyPdf.generic.NumberObject and i < 0:
					text += " "
		elif operator in ['Tf']:
			text += " "

	remove = [u"\u201d", u"\u201c"]
	for r in remove:
		text = text.replace(r, u" ")
	text = text.replace(u"\ufb01", u"fi")

	return text


files = os.listdir(papers_dir)
files = [x for x in files if x[-3:]=='pdf']

titles = []
authors = []
keywords = []
all_papers = []

for i,f in enumerate(files):
	reader = PdfFileReader(open(papers_dir+f, 'rb'))
	print f
	try:
		info = dict(reader.documentInfo)
		try:
			keyword = info['/Keywords'].encode('ascii', 'ignore')
		except:
			keyword=""
		title = info['/Title'].encode('ascii', 'ignore')
		author = info['/Author'].encode('ascii', 'ignore')
		all_papers += [Paper(id_=random.randint(0, 999999999), title=title, authors=author, filename=f, keywords=keyword)]
	except:
		pass
outdict = {}
for p in all_papers:
	outdict[p.paper] = (p.paper, p.title, p.authors, p.filename, p.keywords)

# dump a dictionary indexed by paper id that points to (title, authors) tuple
pickle.dump(outdict, open("papers.p", "wb"))




