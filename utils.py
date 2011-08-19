import os

rootpath = '/path/to/files/'

pdffiles = [i for i in os.listdir(rootpath) if i[-4:] == '.pdf']
