Full text visualisation of a PDF library

Construction of the similarity graph requires three preparative steps:

1) Extract text from the PDF files
2) Build a dictionary
3) Calculate the similarity between documents

Requirements

pdfminer - Used to extract text from PDF files, can be installed with 'pip install pdfminer'
tagger - Used to generate the dictionary and calculate the similarity between documents.  Available from:
	https://github.com/apresta/tagger - compatible with python 2.7
	https://github.com/Torkn/tagger - compatible with python 2.6

Usage

This project is still being actively developed and the usage is currently more convoluted than it could be

1) Alter utils.rootpath to point to the location of your PDF library
2) In database.engine alter the URI for your database
3) Run python pdf2db.py
4) Call generate_dict.build_IDF_dict, optionally specifying any stopwords (currently ignored), a custom reader class and a custom stemmer class (nltk has some worth further investigation) and then dump the results using pickle
	>>> import generate_dict as gd
	>>> import cPickle as pickle
	>>> dictionary = gd.build_IDF_dict(['stop', 'words'])
	>>> pickle.dump(dictionary, open('dictionary.pkl', 'w'))
5) Call calc_similarity.generate_graph_file supplying the location of the dictionary file from step 4, where you want the graph file to be saved and any stop words (again currently ignored)

