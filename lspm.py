#Aline Bessa - 01/05/2010
#Beta version of LSPM
#ARGS: argv[1] - Directory containing files to be tested

from parse_docs import CorpusParser
import sys
import os
import numpy as np
import random

class LSPMSampler(object):
  def __init__(self, a):
    docs = a.pdocs()
    if not docs:
      self.all_words = 0
    else:
      self.all_words = len(docs[0][0])
    self.docs = docs
    self.words = a.words()
    self.list_docs = a.ldocs()
    self.Ndocs = len(self.docs)
    self.dirname = a.dirname()
    self.alpha = 1.0 #supervision level

  def pLi(self, label, index):
    t1 = np.log((self.dccs[label] + self.Gammapi[label])/(len(self.docs) + self.Gammapi[1] + self.Gammapi[0] -1))

    label2 = int(abs(label - 1)) #if pal, get isr; otherwise, get pal.
    t2 = 0.
    for sntc, prsp in zip(self.docs[index], self.labels[index][1]):
      if prsp == 0: continue
      t2 += self.sPi(self.wfreqs[label], self.wfreqs[label2], sntc) 
    return t1 + t2
 
  def pick_label(self, index):
    old = self.labels[index][0]
    self.dccs[old] -= 1
    self.wcounts[old] -= self.rlv_counts[index][1] #Extracting relevant document sentences from its class

    pL0 = self.pLi(0, index)
    pL1 = self.pLi(1, index)
    loglr = pL1-pL0
    lr = np.exp(loglr)
    if lr == np.inf:
      label = 1
    else:
      if np.random.binomial(1, lr/(1+lr)):
        label = 1
      else:
        label = 0
    if label != label:
      print pL0, pL1
      print loglr, lr
      import sys
      sys.exit("nan!")
   
    self.labels[index][0] = label
    self.dccs[label] += 1
    self.wcounts[label] += self.rlv_counts[index][1]
    return label

  def sPi(self, theta, sntc):
  #  p = np.log(p) - np.log(np.sum(p))
    p = sntc*np.log(theta)
 #   p = wcounts + self.Gammatheta
 #   p = np.log(p)
 #   p -= np.sum(p)
 #   p *= sntc
 #   k = (wcounts + self.Gammatheta)/(sum(wcounts + self.Gammatheta))
 #   ent = - sum(k*np.log(k)) 
#    print ent 
    return np.sum(p)

  def prsp(self, prsp, label, sntc):
    if prsp == 0:
     l = 2
   #  counts = self.scounts[2]
   #  wcounts = self.wcounts[2] 
   #  wcounts2 = self.wcounts[label]  
    else:
     l = label
    # counts = self.scounts[label]  
    # wcounts = self.wcounts[label]  
    # wcounts2 = self.wcounts[2] 
    # prior probability of getting a (ir)relevant sentence 
   # prior = np.log((counts + self.Gammatau[prsp])/(self.scounts[label] + self.scounts[2] + self.Gammatau[0] + self.Gammatau[1]))
 #   print "iiiii"
 #   print label 
    return self.sPi(self.theta[l], sntc)

  def pick_prsp(self, j_ind, k_ind):
    old = self.labels[j_ind][1][k_ind]
    self.rlv[j_ind][old] -= 1
    self.rlv_counts[j_ind][old] -= self.docs[j_ind][k_ind]
    if old == 1:  #sentence's prsp == doc_label
      self.wcounts[self.labels[j_ind][0]] -= self.docs[j_ind][k_ind]
      self.scounts[self.labels[j_ind][0]] -= 1
    else:  #sentence has no prsp
      self.wcounts[2] -= self.docs[j_ind][k_ind]
      self.scounts[2] -= 1

    # 0 -> no_prsp; 1 -> prsp == doc_label // doc_label // sentence
    sP0 = self.prsp(0, self.labels[j_ind][0], self.docs[j_ind][k_ind])
    sP1 = self.prsp(1, self.labels[j_ind][0], self.docs[j_ind][k_ind])
  
    loglr = sP1-sP0
    lr = np.exp(loglr)
    p = lr/(1+lr)
#    print "random e p"
#    print k, p
    has_prsp = np.random.binomial(1, p)
    self.labels[j_ind][1][k_ind] = has_prsp
    self.rlv[j_ind][has_prsp] += 1
    self.rlv_counts[j_ind][has_prsp] += self.docs[j_ind][k_ind]
    if has_prsp == 1:
      self.wcounts[self.labels[j_ind][0]] += self.docs[j_ind][k_ind]
      self.scounts[self.labels[j_ind][0]] += 1
    else:
      self.wcounts[2] += self.docs[j_ind][k_ind]
      self.scounts[2] += 1
    return has_prsp

  def likelihood(self):
    lik = 0.
    for i in xrange(len(self.labels)):
      if i >= self.Ndocs * self.alpha:
        lik += self.pLi(self.labels[i][0], i)
      for j in xrange(len(self.labels[i][1])):
        if self.labels[i][1][j]:
          lik += self.sPi(self.theta[self.labels[i][0]], self.docs[i][j])
        else:
          lik += self.sPi(self.theta[2], self.docs[i][j])

    return lik

  def sublist(self, prsp, n):
    t = prsp.items()
    t.sort (key=lambda a:a[1], reverse=True)
    return t[:n]

  def most_common_words(self, n):
    prsp0 = {}
    prsp1 = {}
    no_prsp = {}

    for i in xrange(self.all_words):
      prsp0[self.words[i]] = self.wcounts[0][i]
      prsp1[self.words[i]] = self.wcounts[1][i]
      no_prsp[self.words[i]] = self.wcounts[2][i]

    return self.sublist(prsp0, n), self.sublist(prsp1, n), self.sublist(no_prsp, n)
 
  def get_real_label(self, index):
    #assumptions, assumptions: pal = 1; isr = 0
    filename = os.path.realpath(self.dirname + '/' + self.list_docs[index])
    if filename.find("is") >= 0:
      return 0
    else:
      return 1
 
  def sample(self, nsamples):
    self.Gammapi = np.array([1., 1.])
    self.pi = random.betavariate(1, 1)
    self.Gammatheta = np.array([1. for i in xrange(self.all_words)])
    self.theta = np.zeros((3, self.all_words))
    self.Gammatau = np.array([1., 1.])
    self.dccs = np.zeros(2)
    self.wcounts = np.zeros((3, self.all_words)) #freqs per class (0, 1 or irrelevant)
    self.scounts = np.zeros(3)
    self.rlv = np.zeros((len(self.docs), 2))
    self.rlv_counts = np.zeros((len(self.docs), 2, self.all_words))
    self.tau =  np.array([random.betavariate(1, 1), random.betavariate(1, 1)])
    
    cclass = np.zeros((3, self.all_words))
    for i in xrange(self.Ndocs):
      for j in xrange(len(self.docs[i])):
       cclass[self.get_real_label(i)] += self.docs[i][j]
   
    for i in xrange(self.all_words):
       cclass[2][i] = min(cclass[0][i], cclass[1][i])
       cclass[0][i] = max(0, cclass[0][i] - cclass[2][i])
       cclass[1][i] = max(0, cclass[1][i] - cclass[2][i])

    self.theta[0] = np.random.dirichlet(cclass[0] + self.Gammatheta) 
    self.theta[1] = np.random.dirichlet(cclass[1] + self.Gammatheta) 
    self.theta[2] = np.random.dirichlet(cclass[2] + self.Gammatheta) 
    ###initial document labels and sentence bearing perspectives
    self.labels = []
    for i in xrange(self.Ndocs):
      if i < self.alpha * self.Ndocs:
        label = self.get_real_label(i)
      else:
        label = np.random.binomial(1, self.pi)
      self.dccs[label] += 1
      spbearing = []
      for j in xrange(len(self.docs[i])):
        sP0 = self.sPi(self.theta[2], self.docs[i][j]) 
        sP1 = self.sPi(self.theta[label], self.docs[i][j]) 
        loglr = (sP1-sP0)
        lr = np.exp(loglr)
        p = lr/(1+lr)
        slabel = np.random.binomial(1, p)
        if slabel:
          self.scounts[label] += 1
        else:
          self.scounts[2] += 1
        spbearing.append(slabel)
      self.labels.append([label, spbearing])

    for i in xrange(self.Ndocs):
      for j, a in enumerate(self.labels[i][1]):
        self.rlv[i][a] += 1
        self.rlv_counts[i][a] += self.docs[i][j] #rlv_counts[i][0] => irrelevant; rlv_counts[i][1] => relevant
        if self.labels[i][1][j] == 1:
          self.wcounts[self.labels[i][0]] += self.docs[i][j]
        else:
          self.wcounts[2] += self.docs[i][j]


    ###iterate
    fdocs = open('label_docs.txt', 'w+')
    l =[]
    for i in xrange(nsamples):
      print self.most_common_words(40)[0]
      print self.most_common_words(40)[1]
      print self.most_common_words(40)[2]
   #   a = (self.wcounts[0] + self.Gammatheta)/(np.sum(self.wcounts[0] + self.Gammatheta))
   #   a.sort()
   #   print a[::-1][:20]
   #   a = (self.wcounts[1] + self.Gammatheta)/(np.sum(self.wcounts[1] + self.Gammatheta))
   #   a.sort()
   #   print a[::-1][:20]
   #   a = (self.wcounts[2] + self.Gammatheta)/(np.sum(self.wcounts[2] + self.Gammatheta))
   #   a.sort()
   #   print a[::-1][:20]
      print self.scounts
      print "\n"
      if i % 5 == 0:
        fdocs.write(str(self.most_common_words(40)[0]))
        fdocs.write("\n")
        fdocs.write(str(self.most_common_words(40)[1]))
        fdocs.write("\n")
        fdocs.write(str(self.most_common_words(40)[2]))
        fdocs.write("\n")
      if i % 10 == 0:
        fdocs.write(str(self.likelihood()))
        fdocs.write("\n")
      for j in xrange(self.Ndocs):
        if j >= self.alpha * self.Ndocs:
          new_label = self.pick_label(j)
        else:
          new_label = self.labels[j][0]
        l.append(new_label)
        for k in xrange(len(self.docs[j])):
          self.pick_prsp(j, k)
        
         #      fdocs.write(str(l))
#      fdocs.write("\n")
      l = []
      self.theta[0] = np.random.dirichlet(self.wcounts[0] + self.Gammatheta)
      self.theta[1] = np.random.dirichlet(self.wcounts[1] + self.Gammatheta)
      self.theta[2] = np.random.dirichlet(self.wcounts[2] + self.Gammatheta)
      print i
    fdocs.close()

if __name__=='__main__':
  a = CorpusParser(sys.argv[1])
  b = LSPMSampler(a)
  b.sample(5000)
