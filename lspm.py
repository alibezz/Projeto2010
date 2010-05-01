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

  def pLi(self, label, doc):
    log = np.log
    t1 = log((self.dccs[label] + self.Gammapi[label])/(len(self.docs) + self.Gammapi[1] + self.Gammapi[0] -1))
    t2 = log(((self.sprs[1] + self.Gammatau[1])*(self.sprs[0] + self.Gammatau[0]))/(self.Msents + self.Gammatau[0] + self.Gammatau[1]))
    
    den = np.ones(self.all_words)
    den.fill(np.log(np.sum(self.wccs[label] + self.Gammatheta)))
    t3 = np.sum(log(self.wccs[label] + self.Gammatheta)*doc - den)
    return t1 + t2 + t3
  
  def pick_label(self, index):
    old = self.labels[index][0]
    self.dccs[old] -= 1
    self.sprs[old] -= sum(self.labels[index][1])
    self.Msents -= len(self.docs[index])
    for i in xrange(len(self.docs[index])):
      self.wccs[old] -= self.docs[index][i]

    pL0 = self.pLi(0, self.docs[index])
    pL1 = self.pLi(1, self.docs[index])
    loglr = pL1-pL0
    lr = math.exp(loglr)
    p = lr/(1+lr)
    new = random.random() <= p
    self.dccs[new] += 1
    self.sprs[new] += sum(self.labels[index][1])
    self.Msents += len(self.docs[index])
    for i in xrange(len(self.docs[index])):
      self.wccs[new] += self.docs[index][i]
    return new

  def sPi(self, label, j_ind, k_ind, j_words):
    log = np.log
    t1 = log((sum(self.labels[j_ind][1]) + self.Gammatau[label])/(self.Msents + self.Gammatau[0] + self.Gammatau[1] - 1))

    den = np.ones(self.all_words) 
    den.fill(np.log(np.sum(j_words + self.Gammatheta)))
    t2 =  np.sum(log((1 - label)*j_words + (label - 1)*self.sprs[label] + label*self.sprs[label] + self.Gammatheta)*self.docs[j_ind] - den)
    return t1 + t2

  def pick_prsp(self, label, j_ind, k_ind):
    self.sprs[label] -= self.labels[j_ind][1][k_ind]
    self.labels[j_ind][1][k_ind] = 0
    
    jwords = np.zeros(self.all_words)
    for i in xrange(len(self.docs[j_ind])):
      jwords += self.docs[j_ind][i]
    jwords -= self.docs[j_ind][k_ind]

    sP0 = self.sPi(label, j_ind, k_ind, jwords)
    sP1 = self.sPi(label, j_ind, k_ind, jwords)
    loglr = sP1-sP0
    lr = math.exp(loglr)
    p = lr/(1+lr)
    new = random.random() <= p
    
    self.labels[j_ind][1][k_ind] = new
    self.sprs[label] += self.labels[j_ind][1][k_ind]
    return new
 
  def sample(self, nsamples):
    self.Gammapi = np.array([1., 1.])
    self.pi = random.betavariate(1, 1)
    self.Gammatheta = np.array([1. for i in xrange(self.all_words)])
    self.Gammatau = np.array([1., 1.])
    self.wccs = np.zeros((2, self.all_words))
    self.dccs = np.zeros(2)
    self.sprs = np.zeros(2)

    ###initial document labels and sentence bearing perspectives
    self.labels = []
    self.Msents = 0
    for i in xrange(len(self.docs)):
      label = np.random.binomial(1, self.pi)
      self.dccs[label] += 1
      spbearing = []
      # tau = random.betavariate(1, 1)
      for j in xrange(len(self.docs[i])):
        #more sentences with perspective
        spbearing.append(np.random.binomial(1, 0.7)) 
        self.Msents += 1
      self.labels.append([label, spbearing])
    ###

    ###extracting valuable information
    for i in xrange(len(self.docs)):
      self.sprs[self.labels[i][0]] += sum(self.labels[i][1])
      for j in xrange(len(self.docs[i])):
        self.wccs[self.labels[i][0]] += self.docs[i][j]
    ###

    ###iterate
    for i in xrange(nsamples):
      print self.labels
      print '\n'
      for j in xrange(len(self.docs)): 
        new_label = self.pick_label(j)
        for k in xrange(len(self.docs[j])):
          new_prsp = self.pick_prsp(new_label, j, k) 
    ### 

if __name__=='__main__':
  a = Docs()
  b = LSPMSampler(a.list_docs())
  b.sample(10)
