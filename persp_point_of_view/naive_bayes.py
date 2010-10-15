#Aline Bessa - 27/04/2010
#Naive Bayes modelling for sentiment analysis in docs

import numpy as np
import random
import math
from parse_nb import CorpusParser
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
    print self.all_words
    self.train_dirname = a.train_dirname()
    self.test_dirname = a.test_dirname()
    self.labels = [] 
#    self.alpha = 0.4 #supervision level
    self.Ntraindocs = len(self.train_docs)
    self.Ntestdocs = len(self.test_docs)

  def initial_label(self):
    return np.random.binomial(1, self.pi)

  def get_real_label(self, dir, index):
    #assumptions, assumptions: sit = 1; opos = 0
    ldocs = os.listdir(dir)
    if ldocs[index].find("opos") >= 0:
      return 0
    else:
      return 1

  def label_documents(self):
    for i in xrange(self.Ntraindocs):
      label = self.get_real_label(self.train_dirname, i)
      self.labels.append(label)
    for i in xrange(self.Ntestdocs):
      label = self.initial_label()
      self.labels.append(label)

  def pLi(self, j, doc):
    t1 = np.log((self.dccs[j] + self.Gammapi[j])/(len(self.labels) + self.Gammapi[1] + self.Gammapi[0] -1))
    t2 = doc*np.log(self.theta[j])
    t2 = np.sum(t2)
    return t1+t2


  def pick_label(self, j):
    lclass = self.labels[j]
    self.dccs[lclass] -= 1 
    self.wccs[lclass] -= self.docs[j] 

    pL0 = self.pLi(0, self.docs[j]) 
    pL1 = self.pLi(1, self.docs[j])
    loglr = pL1-pL0
    lr = np.exp(loglr)
    if lr == np.inf:
      label = 1
    else:
      if np.random.binomial(1, lr/(1+lr)):
        label = 1
      else:
        label = 0
    self.labels[j] = label
    self.dccs[label] += 1
    self.wccs[label] += self.docs[j]
    return label
  
  def get_denominator(self):
      den = np.zeros(2)
      for i in range(self.Ntestdocs):
        den[self.get_real_label(self.test_dirname, i)] += 1
      return den

  def num_den(self):
    den = self.get_denominator()
    num = np.zeros(2)
    
    for i in range(self.Ntestdocs):
      l = self.labels[i + self.Ntraindocs] #shifting Ntraindocs positions
      if l == self.get_real_label(self.test_dirname, i):
        num[self.labels[i + self.Ntraindocs]] += 1
    
    return num, den 

  def precision(self, num, den):
    #TP/(TP+FP)
    return num[0]/(num[0] + (den[1] - num[1])), num[1]/(num[1] + (den[0] - num[0]))

  def accuracy(self, num, den):
    return num[0]/den[0], num[1]/den[1], (num[0] + num[1])/(den[0] + den[1])
 
  def sample(self, nsamples):
    self.Gammapi = np.array([1., 1.])
    self.Gammatheta = np.array([1. for i in xrange(self.all_words)])
    self.pi = random.betavariate(1,1)
    self.theta = np.zeros((2, self.all_words)) 
    self.theta[0] = np.random.dirichlet(self.Gammatheta) 
    self.theta[1] = np.random.dirichlet(self.Gammatheta) 
    self.label_documents()
    self.wccs = np.zeros((2, self.all_words))
    self.dccs = np.zeros(2)

    for i, a in enumerate(self.labels):
      self.dccs[a] += 1
      self.wccs[a] += self.docs[i]

    for i in xrange(nsamples):
      for j in xrange(self.Ntestdocs):
        self.pick_label(j + self.Ntraindocs) #shifting Ntraindocs positions
      self.theta[0] = np.random.dirichlet(self.Gammatheta + self.wccs[0])
      self.theta[1] = np.random.dirichlet(self.Gammatheta + self.wccs[1])

      num, den = self.num_den()
      print num[0], num[1]
      print den[0], den[1]
      print "accuracy"
      ac = self.accuracy(num, den)
      print ac
      print "precision"
      pr = self.precision(num, den)
      print pr
      print "f1 measure"
      print 2*pr[0]*ac[0]/(pr[0] + ac[0]), 2*pr[1]*ac[1]/(pr[1] + ac[1]) 

if __name__=='__main__':
  a = CorpusParser(sys.argv[1], sys.argv[2]) 
  s = NaiveBayesSampler(a)
  s.sample(500)
