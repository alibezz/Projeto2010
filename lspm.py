#Aline Bessa - 01/05/2010
#Beta version of LSPM
#ARGS: argv[1] - Directory containing files to be tested

from parse_docs import CorpusParser
import sys
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

  def pLi(self, label, index):
    t1 = np.log((self.dccs[label] + self.Gammapi[label])/(len(self.docs) + self.Gammapi[1] + self.Gammapi[0] -1))

    t2 = 0.
    for sntc, prsp in zip(self.docs[index], self.labels[index][1]):
      if prsp == 0: continue
      t2 += np.sum(np.log(self.wfreqs[label] + self.Gammatheta)*sntc)
      t2 -= np.log(np.sum(self.wfreqs[0] + self.wfreqs[1]+ self.wfreqs[2] + self.Gammatheta))

    return t1 + t2 
 
  def pick_label(self, index):
    old = self.labels[index][0]
    self.dccs[old] -= 1
    self.wfreqs[old] -= self.rlvfreqs[index][1] 
    self.Msents -= len(self.docs[index])

    pL0 = self.pLi(0, index)
    pL1 = self.pLi(1, index)
    loglr = pL1-pL0
    lr = np.exp(loglr)
   # print lr, lr/(1+lr)
    if lr == np.inf:
      label = 1
    else:
      if np.random.binomial(1, lr/(1+lr)):
        label = 0
      else:
        label = 1
    if label != label:
      print pL0, pL1
      print loglr, lr
      import sys
      sys.exit("nan!")
   
    self.labels[index][0] = label
    self.Msents += len(self.docs[index])
    self.dccs[label] += 1
    self.wfreqs[label] += self.rlvfreqs[index][1]
    return label

  def sPi(self, has_prsp, doc_ind, sntc):
    log = np.log
    t1 = log((self.rlv[doc_ind][has_prsp] + self.Gammatau[has_prsp])/(len(self.labels[doc_ind][1]) + self.Gammatau[1] + self.Gammatau[0] -1))
    den = np.ones(self.all_words)
    den.fill(np.log(np.sum(self.rlvfreqs[doc_ind][has_prsp] + self.Gammatheta)))
    t2 = np.sum(log(self.rlvfreqs[doc_ind][has_prsp] + self.Gammatheta)*sntc - den)
    return t1 + t2

  def pick_prsp(self, j_ind, k_ind):
    old = self.labels[j_ind][1][k_ind]
    self.rlv[j_ind][old] -= 1
    self.rlvfreqs[j_ind][old] -= self.docs[j_ind][k_ind]
    #sentence is relevant; wfreqs considers ONLY relevant sentences
    if old == 1:
      self.wfreqs[self.labels[j_ind][0]] -= self.docs[j_ind][k_ind]


    sP0 = self.sPi(0, j_ind, self.docs[j_ind][k_ind])
    sP1 = self.sPi(1, j_ind, self.docs[j_ind][k_ind])
    loglr = sP1-sP0
    lr = np.exp(loglr)
    p = lr/(1+lr)
    has_prsp = random.random() <= p
    self.labels[j_ind][1][k_ind] = has_prsp
    self.rlv[j_ind][has_prsp] += 1
    self.rlvfreqs[j_ind][has_prsp] += self.docs[j_ind][k_ind]
    if has_prsp == 1:
      self.wfreqs[self.labels[j_ind][0]] += self.docs[j_ind][k_ind]
    return has_prsp
 
  def sample(self, nsamples):
    self.Gammapi = np.array([1., 1.])
    self.pi = random.betavariate(1, 1)
    self.Gammatheta = np.array([1. for i in xrange(self.all_words)])
    self.Gammatau = np.array([1., 1.])
    self.dccs = np.zeros(2)
    self.wfreqs = np.zeros((3, self.all_words)) #freqs per class (0, 1 or irrelevant) 
    self.rlv = np.zeros((len(self.docs), 2))
    self.rlvfreqs = np.zeros((len(self.docs), 2, self.all_words))
 
    ###initial document labels and sentence bearing has_has_perspectives
    self.labels = []
    self.Msents = 0
    for i in xrange(len(self.docs)):
      label = np.random.binomial(1, self.pi)
      self.dccs[label] += 1
      spbearing = []
      tau = random.betavariate(1, 1)
      for j in xrange(len(self.docs[i])):
        slabel = np.random.binomial(1, tau)
        spbearing.append(slabel) 
        self.Msents += 1
      self.labels.append([label, spbearing])

    for i in xrange(len(self.docs)):
      for j, a in enumerate(self.labels[i][1]):
        self.rlv[i][a] += 1
        self.rlvfreqs[i][a] += self.docs[i][j]
        if self.labels[i][1][j] == 1:
          self.wfreqs[self.labels[i][0]] += self.docs[i][j]
        else:
          self.wfreqs[2] += self.docs[i][j]

    ###iterate
    fdocs = open('label_docs.txt', 'w+') 
    l =[]
    for i in xrange(nsamples):
      for j in xrange(len(self.docs)): 
        new_label = self.pick_label(j)
        l.append(new_label)
        for k in xrange(len(self.docs[j])):
          self.pick_prsp(j, k) 
      if i % 10 == 0:
        fdocs.write(str(l)) 
      l = []
    fdocs.close()

    flabels = open('all_labels.txt', 'w+')
    flabels.write(str(self.labels))
    flabels.close()
    #for i in xrange(len(self.docs)):
#    print self.docs[8]
#    print self.labels[8][1]

if __name__=='__main__':
  a = CorpusParser(sys.argv[1])
  b = LSPMSampler(a.pdocs())
  b.sample(200)
