import numpy as np
import random
import os
import sys
import math

import re
wre = re.compile(r"[a-zA-Z0-9 ]+")
def get_words(text):
  "A simple tokenizer"
  text = ";".join(text)
  l = 0
  while l < len(text):
    s = wre.search(text,l)
    try:
      yield text[s.start():s.end()]
      l = s.end()
    except:
      break

class NaiveBayesSampler(object):
  def __init__(self):
    self.labels = [] 
    self.docs = []
    self.bags = []
    
    self.all_words = []
    self.Nwords = 0

#OK
  def load_as_bag(self,doc):
        "Creates a bag of words for a single document"
        word_freqs = {}
        #Talvez self.docs fique desnecessario
        for w in get_words(file("/home/alibezz/Desktop/Projeto2010/vectors/"+doc).read().split(" ")):
            w = w.lower()
            if not w in word_freqs:
              word_freqs[w] = 1

            else:
              word_freqs[w] += 1
            if not w in self.all_words:
              self.all_words.append(w)
              self.Nwords += 1
        self.docs.append(word_freqs)

#OK
  def pick_label(self):
    return np.random.binomial(1, self.pi)

#OK
  def label_documents(self):
    for i in xrange(len(self.docs)):
      self.labels.append(self.pick_label())

#OK  
  def makebag(self, i):
    bag = []
    for word in self.all_words:
      if word in self.docs[i]:
        bag.append(self.docs[i][word])
      else:
        bag.append(0)
    return bag  

  def pLi(self, j): 
    log = np.log
    t1 = log((self.dccs[j] + self.Gammapi[j])/(len(self.labels) + self.Gammapi[1] + self.Gammapi[0] -1))
    den = np.ones(len(self.all_words))*self.bags[j]
    den.fill(np.log(np.sum(self.wccs[j] + self.Gammatheta)))
    s = np.sum(log(self.wccs[j] + self.Gammatheta)*self.bags[j] - den)
    return t1+s


  def conddist(self, td): 
    c = self.labels[td]
    self.dccs[c] -= 1 
    self.wccs[c] -= self.bags[td] 

    pL0 = self.pLi(0) 
    pL1 = self.pLi(1)
    loglr = pL1-pL0
    lr = math.exp(loglr)
    p = lr/(1+lr)
    na = random.random() <= p
    self.labels[td] = na
    self.dccs[na] += 1
    self.wccs[na] += self.bags[td]
    return na

  def sample(self, nsamples):
    #initialize
    self.Gammapi = np.array([1., 1.])
    self.Gammatheta = np.array([1. for i in self.all_words])
    self.pi = random.betavariate(1,1)
    self.label_documents()
    self.wccs = np.zeros((2, len(self.all_words)))
    self.dccs = np.zeros(2)
    for i in xrange(len(self.labels)):
      self.bags.append(self.makebag(i))
    for i, a in enumerate(self.labels):
      self.dccs[a] += 1
      self.wccs[a] += self.bags[i]
    ####
   
    for i in xrange(nsamples):
      for j in xrange(len(self.bags)):
        self.conddist(j)
      print self.labels  

if __name__=='__main__':
  docs = os.listdir(sys.argv[1])
  s = NaiveBayesSampler()
  [s.load_as_bag(x) for x in docs]
  s.sample(100)
