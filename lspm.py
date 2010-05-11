#Aline Bessa - 01/05/2010
#Beta version of LSPM

from texts import Docs
import numpy as np
import random
import math

class LSPMSampler(object):
  def __init__(self, docs):
    if not docs:
      self.all_words = 0
    else:
      self.all_words = len(docs[0][0])
    self.docs = docs

  def class_freqs(self, index):
    rlv = np.zeros(2)
    freqs = np.zeros((2, self.all_words))
    for i, a in enumerate(self.labels[index][1]):
      rlv[a] += 1
      freqs[a] += self.docs[index][i]
    return rlv, freqs  

  def pLi(self, label, index, sntcs, freqs):
    log = np.log
    t1 = log((self.dccs[label] + self.Gammapi[label])/(len(self.docs) + self.Gammapi[1] + self.Gammapi[0] -1))

    p = 0.0
    for j in xrange(len(self.docs)):
      if j == index:
        nsents = 0
        sntcs *= 0.0 
      else:
        nsents = len(self.labels[j][1])
      t2 = log((sntcs + self.Gammatau[label])/(nsents + self.Gammatau[1] + self.Gammatau[0] -1))
      
      den = np.ones(self.all_words)
      den.fill(log(sum(freqs + self.Gammatheta)))
      t3 = np.sum(log(freqs + self.Gammatheta) - den)
      p += t2 + t3
    
    return t1 + p
  
  def pick_label(self, index):
    old = self.labels[index][0]
    self.dccs[old] -= 1
    rlv, freqs = self.class_freqs(0)
    for j in xrange(len(self.docs) - 1):
      rlv += self.class_freqs(j+1)[0]
      freqs += self.class_freqs(j+1)[1]

    rlv[0] -= len(self.labels[index][1]) - sum(self.labels[index][1])
    rlv[1] -= sum(self.labels[index][1])
    freqs[old] -= self.wfreqs[index]
  
    pL0 = self.pLi(0, index, rlv[0], freqs[0])
    pL1 = self.pLi(1, index, rlv[1], freqs[1])
    loglr = pL1-pL0
    lr = np.exp(loglr)
    if lr == np.inf:
      p = 1.0
    else:
      p = lr/(1+lr)
    
    if p != p:
      print pL0, pL1
      print loglr, lr
      import sys
      sys.exit("nan!")

    label = random.random() <= p
    print index, p
    self.labels[index][0] = label
    self.dccs[label] += 1
    return label

  def sPi(self, label, sntcs, freq_sntcs, sntc, doc_ind):
    log = np.log
    t1 = log((sntcs + self.Gammatau[label])/(len(self.labels[doc_ind][1]) + self.Gammatau[1] + self.Gammatau[0] -1))
    den = np.ones(self.all_words)
    den.fill(np.log(np.sum(freq_sntcs + self.Gammatheta)))
    s = np.sum(log(freq_sntcs + self.Gammatheta)*sntc - den)
    return t1+s

  def pick_prsp(self, j_ind, k_ind):
    old = self.labels[j_ind][1][k_ind]
    rlv, freqs = self.class_freqs(j_ind)
    rlv[old] -= 1
    freqs[old] -= self.docs[j_ind][k_ind]

    sP0 = self.sPi(0, rlv[0], freqs[0], self.docs[j_ind][k_ind], j_ind)
    sP1 = self.sPi(1, rlv[1], freqs[1], self.docs[j_ind][k_ind], j_ind)
    loglr = sP1-sP0
    lr = np.exp(loglr)
    p = lr/(1+lr)
    label = random.random() <= p
    self.labels[j_ind][1][k_ind] = label
    
    return label
 
  def sample(self, nsamples):
    self.Gammapi = np.array([1., 1.])
    self.pi = random.betavariate(1, 1)
    self.Gammatheta = np.array([1. for i in xrange(self.all_words)])
    self.Gammatau = np.array([1., 1.])
    self.dccs = np.zeros(2)
    self.wfreqs = np.zeros((len(self.docs), self.all_words))

    ###initial document labels and sentence bearing perspectives
    self.labels = []
    self.Msents = 0
    for i in xrange(len(self.docs)):
      label = np.random.binomial(1, self.pi)
      self.dccs[label] += 1
      spbearing = []
      tau = random.betavariate(1, 1)
      for j in xrange(len(self.docs[i])):
        spbearing.append(np.random.binomial(1, tau)) 
        self.Msents += 1
        self.wfreqs[i] += self.docs[i][j]
      self.labels.append([label, spbearing])

    ###iterate
    l =[]
    for i in xrange(nsamples):
      for j in xrange(len(self.docs)): 
        new_label = self.pick_label(j)
        l.append(new_label)
        for k in xrange(len(self.docs[j])):
          self.pick_prsp(j, k) 
     # print l
      l = []
 #    
 #   for i in xrange(len(self.docs)):
 #     print self.docs[i]
 #     print self.labels[i][0]

if __name__=='__main__':
  a = Docs()
  b = LSPMSampler(a.list_docs())
  d = a.list_docs()
  b.sample(20)
