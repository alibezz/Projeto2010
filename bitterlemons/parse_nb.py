#Aline Bessa - 17/05/2010
#This program counts word frequencies within documents and the corpus itself
import sys
import os
import numpy as np
import random
from nltk import *
import en 

stop_words = ['which', 'even', 'can', 'peace', 'than', 'i', 'there', 'one', 'their', 'all', 'they', 'if', 'would', 'more', 'us', 'he', 'its', 'we', 'his', 'from', 'or', 'has', 'have', 'at', 'but', 'are', 'an', 'will', 'not', 'was', 'be', 'by', 'this', 'as', 'the', 'of', 'and', 'to', 'in', 'a', 'that', 'is', 'for', 'quot', 'it', 'on', 'with', 's']

def get_real_label(dir, index):
  #assumptions, assumptions: pal = 1; isr = 0
  ldocs = os.listdir(dir)
  if ldocs[index].find("is") >= 0:
    return 0
  else:
    return 1

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

def bigrams(it):
    prev = None
    for i in it:
        if prev:
            yield prev+" "+i
        prev = i

def skip_bigrams(it, k):
    prevs = deque()
    for i in it:
        if len(prevs) < k:
            prevs.append(i)
        else:
            first = prevs.popleft()
            for j in prevs:
                yield first + " " + j


class CorpusParser(object):
  def __init__(self, train_corpus, test_corpus):
    self.train_corpus = train_corpus
    self.Ntrain_corpus = len(os.listdir(train_corpus))
    self.test_corpus = test_corpus
    self.Ntest_corpus = len(os.listdir(test_corpus))

    self.all_feats = []
    self.all_feats_map = {}
    self.train_list_docs = os.listdir(train_corpus)
    self.test_list_docs = os.listdir(test_corpus)
    self.train_docs = []
    self.test_docs = []

  def chop(self, raw_sntc):
    x =  raw_sntc.find(">") + 1
    y = raw_sntc.find("</")
    return raw_sntc[x:y]

  def feats(self):
    return sorted(self.all_feats)

  def get_sntc(self, sntc):
 #   print self.all_feats
    freqs = np.zeros(len(self.all_feats))
    #TODO Get rid of this repetition
    for t in get_words(sntc):
      t = t.lower().strip()
    #  t = en.noun.singular(t)
      if not t in stop_words:
        freqs[self.all_feats.index(t)] += 1.
    return freqs

  def get_new_words(self, doc):
    for i in xrange(len(doc)):
      for t in get_words(str(doc[i])):
        t = t.lower().strip()
       # t = en.noun.singular(t)
        if not t in self.all_feats and not t in stop_words:
          self.all_feats.append(t)

  def get_bigrams(self, doc, doc_type):
    doc_map = {}
    for i in xrange(len(doc)):
      bigms = bigrams(get_words(str(doc[i])))
      for b in bigms:
        b = b.lower().strip()
        if not b in self.all_feats:
          self.all_feats.append(b)
          self.all_feats_map[b] = self.all_feats.index(b)
        if doc_map.has_key(b):
          doc_map[b] += 1.0
        else:
          doc_map[b] = 1.0
    if doc_type == "train":
      self.train_docs.append(doc_map)
    else:
      self.test_docs.append(doc_map)

  def get_words(self, doc, doc_type):
    doc_map = {}
    for i in xrange(len(doc)):
      words = get_words(str(doc[i]))
      for w in words:
        w = w.lower().strip()
        if not w in self.all_feats:
          self.all_feats.append(w)
          self.all_feats_map[w] = self.all_feats.index(w)
        if doc_map.has_key(w):
          doc_map[w] += 1.0
        else:
          doc_map[w] = 1.0
    if doc_type == "train":
      self.train_docs.append(doc_map)
    else:
      self.test_docs.append(doc_map)


  def docs_train(self):
    return self.train_list_docs

  def docs_test(self):
    return self.test_list_docs

  def train_dirname(self):
    return self.train_corpus

  def test_dirname(self):
    return os.listdir(self.test_corpus)

  def get_doc(self, doc):
    counts = np.zeros(len(self.all_feats))
    for sntc in doc:
      for t in bigrams(sntc):
        t = t.lower().strip()
       # t = en.noun.singular(t)
        if not t in stop_words and t in self.all_feats:
          counts[self.all_feats.index(t)] += 1.
    return counts

  def pdocs(self):

    ###feats acquisition
    for file in self.train_list_docs:
      f = open(os.path.realpath(self.train_corpus + '/' + file), 'r')
      doc = read_file(f)
      self.get_bigrams(doc, "train")
      f.close()
    for file in self.test_list_docs:
      f = open(os.path.realpath(self.test_corpus + '/' + file), 'r')
      doc = read_file(f)
      self.get_bigrams(doc, "test")
      f.close()
    ###

#    ###documents as word counts
#    for file in self.train_list_docs:
#      #TODO get rid of repetition
#      f = open(os.path.realpath(self.train_corpus + '/' + file), 'r')
#      doc = read_file(f)
#      self.train_docs.append(self.get_doc(doc))
#      f.close()
#
#    for file in self.test_list_docs:
#      #TODO get rid of repetition
#      f = open(os.path.realpath(self.test_corpus + '/' + file), 'r')
#      doc = read_file(f)
#      self.test_docs.append(self.get_doc(doc))
#      f.close()
#    ###

  #  print self.all_feats, len(self.all_words)
    return self.train_docs, self.test_docs

if __name__ =='__main__':
  a = CorpusParser(sys.argv[1], sys.argv[2])
  training, testing = a.pdocs()
  all_feats = a.feats()
  print training
  print testing
#  f = open("out.txt", 'w+')
#  for i in xrange(len(training)):
#    f.write(str(get_real_label(sys.argv[1], i)) + "\t")
#    keys = sorted(training[i].keys())
#    for feat in keys:
#      f.write("F"+str(all_feats.index(feat)) + " " + str(training[i][feat]) + " ")
#    f.write("\n")
#
#  f.write("DEV\n")
#  #FIXME write only once
#  for i in xrange(len(testing)):
#    f.write(str(get_real_label(sys.argv[1], i)) + "\t")
#    keys = sorted(testing[i].keys())
#    for feat in keys:
#      f.write("F"+str(all_feats.index(feat)) + " " + str(testing[i][feat]) + " ")
#    f.write("\n")
#
#  f.close()        
#
