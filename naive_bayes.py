#Aline Bessa - 27/04/2010
#Naive Bayes modelling for sentiment analysis in docs

import numpy as np
import random
import math

class NaiveBayesSampler(object):
  def __init__(self, docs):
    if not docs.any(): 
      self.all_words = 0
    else:
      self.all_words = len(docs[0])
    self.labels = [] 
    self.docs = docs

  def pick_label(self):
    return np.random.binomial(1, self.pi)

  def label_documents(self):
    for i in xrange(len(self.docs)):
      self.labels.append(self.pick_label())

  def pLi(self, j, doc):
    log = np.log
    t1 = log((self.dccs[j] + self.Gammapi[j])/(len(self.labels) + self.Gammapi[1] + self.Gammapi[0] -1))
    den = np.ones(self.all_words)
    den.fill(np.log(np.sum(self.wccs[j] + self.Gammatheta)))
    s = np.sum(log(self.wccs[j] + self.Gammatheta)*doc - den)
    return t1+s


  def conddist(self, td):
    c = self.labels[td]
    self.dccs[c] -= 1 
    self.wccs[c] -= self.docs[td] 

    pL0 = self.pLi(0, self.docs[td]) 
    pL1 = self.pLi(1, self.docs[td])
    loglr = pL1-pL0
    lr = math.exp(loglr)
    p = lr/(1+lr)
    na = random.random() <= p
    self.labels[td] = na
    self.dccs[na] += 1
    self.wccs[na] += self.docs[td]
    return na

  def sample(self, nsamples):
    self.Gammapi = np.array([1., 1.])
    self.Gammatheta = np.array([1. for i in xrange(self.all_words)])
    self.pi = random.betavariate(1,1)
    self.label_documents()
    self.wccs = np.zeros((2, self.all_words))
    self.dccs = np.zeros(2)

    for i, a in enumerate(self.labels):
      self.dccs[a] += 1
      self.wccs[a] += self.docs[i]
    print self.wccs
    for i in xrange(nsamples):
      for j in xrange(len(self.docs)):
        self.conddist(j)
      print self.labels

if __name__=='__main__':
  docs = np.array([
[0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
[1, 1, 0, 1, 1, 0, 0, 1, 0, 0],
[1, 1, 1, 0, 1, 0, 1, 0, 0, 0],
[1, 0, 0, 0, 0, 1, 1, 1, 1, 0],
[0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
[0, 0, 1, 0, 0, 1, 1, 0, 1, 1],
[0, 0, 0, 1, 0, 1, 0, 1, 1, 1],
], dtype=np.float32)
 
  s = NaiveBayesSampler(docs)
  s.sample(30)
