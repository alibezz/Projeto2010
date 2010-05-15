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

  def pLi(self, label, index):
    t1 = np.log((self.dccs[label] + self.Gammapi[label])/(len(self.docs) + self.Gammapi[1] + self.Gammapi[0] -1))

    t2 = 0.
    for sntc, prsp in zip(self.docs[index], self.labels[index][1]):
      if prsp == 0: continue
      t2 += np.sum(np.log(self.wfreqs[label] + self.Gammatheta)*sntc)
      t2 -= np.log(np.sum(self.wfreqs[0] + self.wfreqs[1]+ self.wfreqs[2] + self.Gammatheta))

    return t1 + t2 
#    for i in xrange(len(self.docs)):
#      if i != index and self.labels[i][0] == label: #it doesn't consider the document itself and only counts for docs in the class
#        tdoc = log((self.prsp[i] + self.Gammatau[i])/self.Msents + self.Gammatau[0] + self.Gammatau[1])
#        tsents = 0.0
#        for j in xrange(len(self.docs[i])):
#          if self.labels[i][1][j] == 1: #sentence has perspective
#            tsents += LOG
##    t2 = log(((self.prsp[0] + self.Gammatau[0])*(self.prsp[1] + self.Gammatau[1]))/self.Msents + self.Gammatau[0] + self.Gammatau[1])
#    den = np.ones(self.all_words)
#    den.fill(np.log(np.sum(self.wfreqs[label] + self.Gammatheta)))
#    print self.wfreqs[label] + self.Gammatheta
#    print self.rlvfreqs[index][1]
#    t3 = np.sum(log(self.wfreqs[label] + self.Gammatheta)*self.rlvfreqs[index][1] - den)
#    print t1, t2, t3 
# 
#    return t1 + t2 + t3
  
  def pick_label(self, index):
    old = self.labels[index][0]
    self.dccs[old] -= 1
    self.wfreqs[old] -= self.rlvfreqs[index][1] #retira todas as frases relevantes 
    self.Msents -= len(self.docs[index])
    #FALTAM TODAS AS FRASES RELEVANTES NA CLASSE ZERO E UM EXCETUANDO O DOC! SOMA E FREQS!
   # print 'iiii'
   # print old
   # print self.wfreqs[old]
   # print self.rlvfreqs[index][1]
   # print 'jjjj' 
   # rlv[0] -= len(self.labels[index][1]) - sum(self.labels[index][1])
   # rlv[1] -= sum(self.labels[index][1])
   # freqs[old] -= self.wfreqs[index]
  
    # self.rlv[index][1] sao todas as frases com has_has_perspectiva no documento
    #self.rlvfreqs[index][1] eh a freq. de todas as palavras em frases relevantes dos documentos

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
    s = np.sum(log(self.rlvfreqs[doc_ind][has_prsp] + self.Gammatheta)*sntc - den)
    return t1+s

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
    #redundante
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
    self.prsp = np.zeros(len(self.docs))
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
          self.prsp[i] += 1
          self.wfreqs[self.labels[i][0]] += self.docs[i][j]
        else:
          self.wfreqs[2] += self.docs[i][j]
    ###iterate
    l =[]
    for i in xrange(nsamples):
      for j in xrange(len(self.docs)): 
        new_label = self.pick_label(j)
        l.append(new_label)
        for k in xrange(len(self.docs[j])):
          self.pick_prsp(j, k) 
      print l
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
