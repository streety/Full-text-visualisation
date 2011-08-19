import os
import multiprocessing, signal

import utils
import pdf
from database import db_session
from models import *

def process_pdfs(rootpath):
	"""Walk through all directories beneath rootpath and extract text from any pdf files found"""
	timeouts = []
	errors = []
	for root, dirs, files in os.walk(rootpath):
		directory = Directory(root)
		db_session.add(directory)
		db_session.commit()
		print 'Converting files in: %s' % (root)
		for name in files:
			if name[-4:] == '.pdf':
				try:
					if already_processed(name, root):
						print 'Already converted: %s' % (name)
						continue
					print 'Converting: %s' % (name)
					doc = Document(name)
					doc.directory_id = directory.id
					q = multiprocessing.Queue()
					p = multiprocessing.Process(target=extract_pages, args=(os.path.join(root, name), q,))
					p.start()
					p.join(timeout=5*60)
					if p.is_alive():
						# Timeout has expired
						p.terminate()
						print 'Processing timeout: %s' % name
						timeouts.append({'dir':root, 'file':name})
						continue
					pages = q.get()
					if not pages:
						print 'Error processing: %s' % name
						errors.append({'dir':root, 'file':name})
						continue
					for i, text in enumerate(pages):
						page = Page(text, i)
						doc.pages.append(page)
					db_session.add(doc)
					db_session.commit()
				except:
					print 'Error processing: %s' % name
					errors.append({'dir':root, 'file':name})
			else:
				print 'Skipping: %s' % (name)
		db_session.add(directory)
		db_session.commit()
		return {'timeouts':timeouts, 'errors':errors}

def already_processed(name, directory):
	"""Check whether a document has already been processed"""
	dbcheck = Document.query.filter(Document.filename == name).all()
	for doc in dbcheck:
		if doc.directory.directory == directory:
			return True
	return False

def extract_pages(filename, q):
	"""Extract text from the pdf file filename"""
	try:
		pages = pdf.get_pages(filename)
		q.put(pages)
	except:
		q.put(False)

if __name__ == '__main__':
	missed = process_pdfs(utils.rootpath)
	print missed
	print 'Timeouts: ', len(missed['timeouts'])
	print 'Errors: ', len(missed['errors'])