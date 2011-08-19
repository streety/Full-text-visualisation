from generate_dict import UnicodeReader
from tagger.tagger import Stemmer
import collections
import os
import cPickle as pickle

from models import *

def generate_tf_idf(dictionary, text, stopwords, reader=UnicodeReader(), stemmer=Stemmer()):
	"""Generate a dictionary with stemmed word counts for a piece of text"""
	words = [w.stem for w in map(stemmer, reader(text))]
	term_count = collections.defaultdict(int)
	for w in words:
		term_count[w] += 1
	dict_out = {}
	for w, cnt in term_count.iteritems():
		if w in dictionary:
			dict_out[w] = dictionary[w] * cnt
	return dict_out

def compare_tf_idf(dictionary1, dictionary2):
	total = 0.
	for w, score in dictionary1.iteritems():
		if w in dictionary2:
			total += score * dictionary2[w]
	return total

def generate_graph_file(dictionary_file, graph_file, stopwords=[]):
	dictionary = pickle.load(open(dictionary_file, 'rb'))
	docs = Document.query.all()
	all_tf_idf = {}
	cached_tf_idf = os.listdir('tf_idf')
	for doc in docs:
		filename = 'tf_idf_doc' + str(doc.id) + '.pkl'
		if filename not in cached_tf_idf:
			print 'No cache found for %s' % filename
			text = ' '.join([i.body for i in doc.pages.all()])
			tf_idf = generate_tf_idf(dictionary, text, stopwords)
			pickle.dump(tf_idf, 	\
				open('tf_idf/' + filename, 'w'))
		else:
			print 'Loading pickle %s' % filename
			tf_idf = pickle.load(open('tf_idf/' + filename, 'rb'))
		all_tf_idf[doc.id] = tf_idf
	print "tf_idf's loaded"
	results = ''
	keys = all_tf_idf.keys()
	keys.sort()
	for key in keys:
		print key
		results += str(key)
		max_score = compare_tf_idf(all_tf_idf[key], all_tf_idf[key])
		if max_score == 0:
			results += "\n"
			continue
		scores = {}
		for id_num, tf_idf in all_tf_idf.iteritems():
			score = compare_tf_idf(all_tf_idf[key], tf_idf) / max_score
			scores[id_num] = score
		score_vals = scores.values()
		score_vals.sort()
		cutoff = 0.8
		if score_vals[-5] > cutoff: cutoff = score_vals[-5]
		for id_num, score in scores.iteritems():
			if (score >= cutoff) and (id_num != key):
				results += ',' + str(id_num)
		results += "\n"
	return results


