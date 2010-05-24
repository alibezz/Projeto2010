#Aline Bessa - 17/05/2010
#This program counts word frequencies within documents,
#sentences and the corpus itself
import sys
import os
from BeautifulSoup import BeautifulSoup
import numpy as np

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

  def chop(self, raw_sntc):
    x =  raw_sntc.find(">") + 1
    y = raw_sntc.find("</")
    return raw_sntc[x:y]

  def get_sntc(self, sntc):
 #   print self.all_words
    freqs = np.zeros(len(self.all_words))
    #TODO Get rid of this repetition
    for t in get_words(sntc):
      t = t.lower().strip()
      freqs[self.all_words.index(t)] += 1.
    return freqs
 
  def get_new_words(self, doc):
    for i in xrange(len(doc)):
      for t in get_words(self.chop(str(doc[i]))):
        t = t.lower().strip()
        if not t in self.all_words:
          #stemming version
          #t = PorterStemmer().stem_word(t)
          #lemmatizing version
          #t = en.noun.singular(t)
          self.all_words.append(t)

  def get_doc(self, doc):
    sntcs = []
    for i in xrange(len(doc)):
      sntcs.append(self.get_sntc(self.chop(str(doc[i])))) 
    return sntcs

  def pdocs(self):
    for file in os.listdir(self.corpus):
      f = open(os.path.realpath(self.corpus + '/' + file), 'r')
      text = read_file(f)
      doc = BeautifulSoup(''.join(text)).contents[1].findAll('s')
      self.get_new_words(doc)
      f.close()
    
    self.docs = []
    for file in os.listdir(self.corpus):
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
