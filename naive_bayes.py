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
    self.docs = a.pdocs()
    if not self.docs: 
      self.all_words = 0
    else:
      self.all_words = len(self.docs[0])
    self.dirname = a.dirname()
    self.labels = [] 
    self.alpha = 0.3 #supervision level
    self.Ndocs = len(self.docs)
    self.list_docs = a.ldocs()

  def initial_label(self):
    return np.random.binomial(1, self.pi)

  def get_real_label(self, index):
    #assumptions, assumptions: pal = 1; isr = 0
    filename = os.path.realpath(self.dirname + '/' + self.list_docs[index])
    if filename.find("is") >= 0:
      return 0
    else:
      return 1

  def label_documents(self):
    for i in xrange(self.Ndocs):
      if i < self.alpha * self.Ndocs:
        label = self.get_real_label(i)
      else:
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
    lr = math.exp(loglr)
    p = lr/(1+lr)
    new = random.random() <= p
    self.labels[j] = new
    self.dccs[new] += 1
    self.wccs[new] += self.docs[j]
    return new
  
  def get_denominator(self, first):
      den = np.zeros(2)
      for i in range(first, self.Ndocs - 1):
        den[self.get_real_label(i)] += 1
      return den

  def accuracy(self):
    first_sampled = math.ceil(self.alpha * self.Ndocs)
    den = self.get_denominator(first_sampled)
    num = np.zeros(2)
    
    for i in range(first_sampled, self.Ndocs - 1):
      l = self.labels[i]
      if l == self.get_real_label(i):
        num[self.labels[i]] += 1

#    print num, den
    return num[0]/den[0], num[1]/den[1]

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
      for j in xrange(self.Ndocs):
        if j < self.alpha * self.Ndocs:
          self.get_real_label(j)
        else:
          self.pick_label(j)
      self.theta[0] = np.random.dirichlet(self.Gammatheta + self.wccs[0])
      self.theta[1] = np.random.dirichlet(self.Gammatheta + self.wccs[1])
      print self.accuracy()
 

if __name__=='__main__':
 # docs = np.array([
#[0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
#[1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
#[1, 1, 0, 1, 1, 0, 0, 1, 0, 0],
#[1, 1, 1, 0, 1, 0, 1, 0, 0, 0],
#[1, 0, 0, 0, 0, 1, 1, 1, 1, 0],
#[0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
#[0, 0, 1, 0, 0, 1, 1, 0, 1, 1],
#[0, 0, 0, 1, 0, 1, 0, 1, 1, 1],
#], dtype=np.float32)
  a = CorpusParser(sys.argv[1]) 
  s = NaiveBayesSampler(a)
  s.sample(150)
