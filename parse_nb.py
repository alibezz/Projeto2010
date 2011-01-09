#Aline Bessa - 17/05/2010
import sys
import os
import numpy as np
import random
from nltk import *

stop_words = [] #['which', 'even', 'can', 'peace', 'than', 'i', 'there', 'one', 'their', 'all', 'they', 'if', 'would', 'more', 'us', 'he', 'its', 'we', 'his', 'from', 'or', 'has', 'have', 'at', 'but', 'are', 'an', 'will', 'not', 'was', 'be', 'by', 'this', 'as', 'the', 'of', 'and', 'to', 'in', 'a', 'that', 'is', 'for', 'quot', 'it', 'on', 'with', 's']

def read_file(file):
   text = []
   line = file.readline()
   while(line != ""):
     text.append(str(line).strip())
     line = file.readline()
   return text

def get_words(text):
  import re
  wre = re.compile(r"(\w)+")
  l = 0
  while l < len(text):
       s = wre.search(text,l)
       try:
           yield text[s.start():s.end()]
           l = s.end()
       except:
           break

class CorpusParser(object):
  def __init__(self, train_corpus, test_corpus):
    self.train_corpus = train_corpus
    self.Ntrain_corpus = len(os.listdir(train_corpus))
    self.test_corpus = test_corpus
    self.Ntest_corpus = len(os.listdir(test_corpus))
    self.train_list_docs = os.listdir(train_corpus)
    self.test_list_docs = os.listdir(test_corpus)
    self.train_docs = []
    self.test_docs = []

    self.all_words = []
# random.shuffle(self.list_docs)

  def train_dirname(self):
    return self.train_corpus
  def test_dirname(self):
    return self.test_corpus

  def chop(self, raw_sntc):
    x = raw_sntc.find(">") + 1
    y = raw_sntc.find("</")
    return raw_sntc[x:y]

  def words(self):
    return self.all_words

  def get_new_words(self, doc):
    for i in xrange(len(doc)):
      for t in get_words(str(doc[i])):
        t = t.lower().strip()
       # t = en.noun.singular(t)
        if not t in self.all_words and not t in stop_words:
          self.all_words.append(t)

  def ldocs(self):
    return self.list_docs

  def dirname(self):
    return self.corpus

  def get_doc(self, doc):
    counts = np.zeros(len(self.all_words))
    for sntc in doc:
      for t in get_words(sntc):
        t = t.lower().strip()
       # t = en.noun.singular(t)
        if not t in stop_words and t in self.all_words:
          counts[self.all_words.index(t)] += 1.
    return counts

  #TODO cut redundancy between docs and dir params
  def iterate_corpus(self, docs, dir, action, doc_preprocessing = None):
    for file in docs:
      f = open(os.path.realpath(dir + '/' + file), 'r')
      doc = read_file(f)
      if doc_preprocessing:
        action(doc_preprocessing(doc))
      else:
        action(doc)
      f.close()


  ###get every single word first
  def pdocs(self):

    self.iterate_corpus(self.train_list_docs, self.train_corpus, self.get_new_words)
    self.iterate_corpus(self.test_list_docs, self.test_corpus, self.get_new_words)
    self.iterate_corpus(self.train_list_docs, self.train_corpus, self.train_docs.append, self.get_doc)
    self.iterate_corpus(self.test_list_docs, self.test_corpus, self.test_docs.append, self.get_doc)
    return self.train_docs, self.test_docs
 # print self.all_words, len(self.all_words)

if __name__ =='__main__':
  a = CorpusParser(sys.argv[1], sys.argv[2])
  a.pdocs()


