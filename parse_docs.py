#Aline Bessa - 17/05/2010
#This program counts word frequencies within documents,
#sentences and the corpus itself
import sys
import os
from BeautifulSoup import BeautifulSoup

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
    "get frequencies of words per sentence"

  def get_new_words(self, text):
    for i in text:
      for t in get_words(i):
        t = t.lower().strip()
        if not t in self.all_words:
          #stemming version
          #t = PorterStemmer().stem_word(t)
          #lemmatizing version
          #t = en.noun.singular(t)
          self.all_words.append(t)

  def get_doc(self, text):
    doc = BeautifulSoup(''.join(text)).contents[1].findAll('s')
    sntcs = []
    for i in xrange(len(doc)):
      sntcs.append(self.get_sntc(self.chop(doc[i]))) 


  def pdocs(self):
    for file in os.listdir(self.corpus):
      f = open(os.path.realpath(self.corpus + '/' + file), 'r')
      text = read_file(f)
          # print text
      self.get_new_words(text)
      self.get_doc(text)
      f.close()
    #print self.all_words

if __name__ =='__main__':
  a = CorpusParser(sys.argv[1])
  a.pdocs()
