import pyPdf
from pyPdf import PdfFileReader
import os
from IPython import embed

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


files = os.listdir('.')
files = [x for x in files if x[-3:]=='pdf']
text_out = open('all_text.txt', 'w')
# text_out = open('all_titles.txt', 'w')

titles = []
authors = []
keywords = []
body = []


for i,f in enumerate(files):
	reader = PdfFileReader(open(f, 'rb'))
	info = dict(reader.documentInfo)
	titles += [info['/Title']]
	authors += [info['/Author']]
	keywords += [info['/Keywords']]

	content = ""
	for p in range(reader.numPages):
		page = reader.getPage(p)
		content += get_text(page)

	if i == 0:
		embed()
	body += [content]

for b in body:
	text_out.write(b.encode("ascii", "ignore"))
# for t in titles:
	# text_out.write(t+"\n-\n\n")
text_out.close()




