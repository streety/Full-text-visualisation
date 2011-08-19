from sqlalchemy import Table, Column, Boolean, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import Base

class Directory(Base):
	__tablename__ = 'directory'
	id = Column(Integer, primary_key=True)
	directory = Column(Text)

	def __init__ (self, directory=None):
		self.directory = directory


class Document(Base):
	__tablename__ = 'document'
	id = Column(Integer, primary_key=True)
	filename = Column(Text)
	title = Column(Text)
	abstract = Column(Text)

	directory_id = Column(Integer, ForeignKey(Directory.id))
	directory = relationship('Directory', backref=backref('documents', order_by=id))

	def __init__(self, filename=None, title=None, abstract=None):
		self.filename = filename
		self.title = title
		self.abstract = abstract


class Page(Base):
	__tablename__ = 'page'
	id = Column(Integer, primary_key=True)
	body = Column(Text)
	pagenum = Column(Integer)

	document_id = Column(Integer, ForeignKey(Document.id))
	document = relationship('Document', backref=backref('pages', order_by=pagenum, lazy='dynamic'))

	def __init__ (self, body=None, pagenum=None):
		self.body = body
		self.pagenum = pagenum

tagdocument = Table(
    'tagdocument', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('document_id', Integer, ForeignKey('document.id'))
    )

class Tag(Base):
	__tablename__ = 'tag'
	id = Column(Integer, primary_key=True)
	tag = Column(String(100))

	documents = relationship('Document', secondary=tagdocument, backref=backref('tags', order_by=id))

	def __init__ (self, tag=None):
		self.tag = tag

authordocument = Table(
    'authordocument', Base.metadata,
    Column('author_id', Integer, ForeignKey('author.id')),
    Column('document_id', Integer, ForeignKey('document.id'))
    )

class Author(Base):
	__tablename__ = 'author'
	id = Column(Integer, primary_key=True)
	firstname = Column(String(100))
	lastname = Column(String(100))

	documents = relationship('Document', secondary=authordocument, backref=backref('authors', order_by=id))

