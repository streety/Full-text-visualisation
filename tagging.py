from database import db_session
from models import *

import cPickle as pickle
from tagger import tagger

docs = Document.query.all()

weights = pickle.load(open('tagger/data/dict.pkl', 'rb')) # or your own dictionary
myreader = tagger.Reader() # or your own reader class
mystemmer = tagger.Stemmer() # or your own stemmer class
myrater = tagger.Rater(weights) # or your own... (you got the idea)
mytagger = Tagger(myreader, mystemmer, myrater)


for doc in docs:
	txt = '\n\n'.join([i.body for i in doc.pages])
	tags = mytagger(txt, 5)
	for tag in tags:
		qry = Tag.query.filter_by(Tag.tag == tag).first()
		if qry:
			doc.tags.append(qry)
		else:
			doc.tags.append(Tag(tag))
	db_session.add(doc)
	db_session.commit()