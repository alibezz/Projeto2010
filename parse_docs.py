#Aline Bessa - 17/05/2010
#This program counts word frequencies within documents,
#sentences and the corpus itself
import sys
import os
from BeautifulSoup import BeautifulSoup
import numpy as np
import random
from nltk import *
import en 

stop_words = ['which', 'even', 'can', 'peace', 'than', 'i', 'there', 'one', 'their', 'all', 'they', 'if', 'would', 'more', 'us', 'he', 'its', 'we', 'his', 'from', 'or', 'has', 'have', 'at', 'but', 'are', 'an', 'will', 'not', 'was', 'be', 'by', 'this', 'as', 'the', 'of', 'and', 'to', 'in', 'a', 'that', 'is', 'for', 'quot', 'it', 'on', 'with', 's']

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
  def __init__(self, corpus):
    self.corpus = corpus
    self.Ncorpus = len(os.listdir(corpus))
    self.all_words = []
    self.docs= []
    self.list_docs = os.listdir(corpus)
    random.shuffle(self.list_docs)

  def chop(self, raw_sntc):
    x =  raw_sntc.find(">") + 1
    y = raw_sntc.find("</")
    return raw_sntc[x:y]

  def words(self):
    return self.all_words

  def get_sntc(self, sntc):
 #   print self.all_words
    freqs = np.zeros(len(self.all_words))
    #TODO Get rid of this repetition
    for t in get_words(sntc):
      t = t.lower().strip()
      t = en.noun.singular(t)
      if not t in stop_words:
        freqs[self.all_words.index(t)] += 1.
    return freqs

  def get_new_words(self, doc):
    for i in xrange(len(doc)):
      for t in get_words(self.chop(str(doc[i]))):
        t = t.lower().strip()
        t = en.noun.singular(t)
        if not t in self.all_words and not t in stop_words:
          self.all_words.append(t)

  def ldocs(self):
    return self.list_docs

  def dirname(self):
    return self.corpus

  def get_doc(self, doc):
    sntcs = []
    for i in xrange(len(doc)):
      sntcs.append(self.get_sntc(self.chop(str(doc[i]))))
    return sntcs

  def pdocs(self):
    for file in self.list_docs:
      f = open(os.path.realpath(self.corpus + '/' + file), 'r')
      text = read_file(f)
      doc = BeautifulSoup(''.join(text)).contents[1].findAll('s')
      self.get_new_words(doc)
      f.close()

    self.docs = []
    for file in self.list_docs:
      #TODO get rid of repetition
      f = open(os.path.realpath(self.corpus + '/' + file), 'r')
      text = read_file(f)
      doc = BeautifulSoup(''.join(text)).contents[1].findAll('s')
      ##
      self.docs.append(self.get_doc(doc))
      f.close()

  #  print self.all_words, len(self.all_words)
    return self.docs

if __name__ =='__main__':
  a = CorpusParser(sys.argv[1])
  a.pdocs()

