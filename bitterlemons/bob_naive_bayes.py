#Aline Bessa - 27/04/2010
#Naive Bayes modelling for sentiment analysis in docs

import numpy as np
import random
import math
from bob_parse_nb import CorpusParser
import sys
import os

class NaiveBayesSampler(object):
  def __init__(self, a):
    pdocs = a.pdocs()
    self.train_docs = pdocs[0]
    self.test_docs = pdocs[1]
    self.docs = self.train_docs + self.test_docs
    if not self.docs: 
      self.all_words = 0
    else:
      self.all_words = len(self.docs[0])
    self.words = a.feats_map()
    self.train_dirname = a.train_dirname()
    self.test_dirname = a.test_dirname()
    self.labels = [] 
#    self.alpha = 0.4 #supervision level
    self.Ntraindocs = len(self.train_docs)
    self.Ntestdocs = len(self.test_docs)

  def initial_label(self):
    return np.random.binomial(1, self.pi)

  def get_real_label(self, dir, index):
    #assumptions, assumptions: pal = 1; isr = 0
    ldocs = os.listdir(dir)
    if ldocs[index].find("is") >= 0:
      return 0
    else:
      return 1

  def label_documents(self):
    for i in xrange(self.Ntraindocs):
      self.labels.append(self.get_real_label(self.train_dirname, i))
    for i in xrange(self.Ntestdocs):
      self.labels.append(self.initial_label())

  def pLi(self, label, doc):
    t1 = np.log((self.dccs[label] + self.Gammapi[label])/(len(self.labels) + self.Gammapi[1] + self.Gammapi[0] -1))
    
    num = 1.0
    keys = doc.keys()
    for w in keys:
      for i in xrange(int(doc[w])): #i eh o no de vezes que w ocorre em doc
        if self.wccs[label].has_key(w):
          num *= 1 + i + self.wccs[label][w] #1 eh o hiperp. pra todas as palavras 
        else:
          num *= 1 + i  
    den = 1.0
    words_keys = self.words.keys()
    for j in xrange(len(keys)):
      sum = 0.0
      for w in words_keys:
        if self.wccs[label].has_key(w):
          sum += 1 + j + self.wccs[label][w]
        else:
          sum += 1 + j
      den *= sum
    t2 = np.log(num/den)
    return t1+t2

  def sum_doc(self, label, index):
    doc_keys = self.docs[index].keys()
    for k in doc_keys:
      if self.wccs[label].has_key(k):
        self.wccs[label][k] += 1.0
      else:
        self.wccs[label][k] = 1.0

  def reduce_doc(self, label, index):
    doc_keys = self.docs[index].keys()
    for k in doc_keys:
      if self.wccs[label].has_key(k):
        self.wccs[label][k] += 1.0
      else:
        self.wccs[label][k] = 1.0

  def pick_label(self, j):
    lclass = self.labels[j]
    self.dccs[lclass] -= 1 
    self.reduce_doc(lclass, j) 

    pL0 = self.pLi(0, self.docs[j]) 
    pL1 = self.pLi(1, self.docs[j])
    loglr = pL1-pL0
    lr = math.exp(loglr)
    p = lr/(1+lr)
    new = random.random() <= p
    self.labels[j] = new
    self.dccs[new] += 1
    self.sum_doc(new, j)
    return new
  
  def get_denominator(self):
      den = np.zeros(2)
      for i in range(self.Ntestdocs):
        den[self.get_real_label(self.train_dirname, i)] += 1
      return den

  def accuracy(self):
    den = self.get_denominator()
    num = np.zeros(2)
    
    for i in range(self.Ntestdocs):
      l = self.labels[i + self.Ntraindocs] #shifting Ntraindocs positions
      if l == self.get_real_label(self.test_dirname, i):
        num[self.labels[i + self.Ntraindocs]] += 1
    
    return num[0]/den[0], num[1]/den[1]
  def sample(self, nsamples):
    self.Gammapi = np.array([1., 1.])
    self.Gammatheta = np.array([1. for i in xrange(self.all_words)])
    self.pi = random.betavariate(1,1)
    self.theta = np.zeros((2, self.all_words)) 
    self.theta[0] = np.random.dirichlet(self.Gammatheta) 
    self.theta[1] = np.random.dirichlet(self.Gammatheta) 
    self.label_documents()
    self.wccs = [{},{}]
    self.dccs = np.zeros(2)

    for i, a in enumerate(self.labels):
      self.dccs[a] += 1
      self.sum_doc(a,i)

    for i in xrange(nsamples):
      for j in xrange(self.Ntestdocs):
        self.pick_label(j + self.Ntraindocs) #shifting Ntraindocs positions
    #  self.theta[0] = np.random.dirichlet(self.Gammatheta + self.wccs[0])
     # self.theta[1] = np.random.dirichlet(self.Gammatheta + self.wccs[1])
      print self.accuracy()
 

if __name__=='__main__':
  a = CorpusParser(sys.argv[1], sys.argv[2]) 
  s = NaiveBayesSampler(a)
  s.sample(200)
