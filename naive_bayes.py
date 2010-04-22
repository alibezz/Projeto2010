import numpy as np
import random
import os
import sys

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
    self.c0 = []
    self.c1 = []
    self.labels = {} 
    self.docs = []
    
    self.all_words = []
    self.Nwords = 0
    self.docs_freqs = []
    self.reverse_map = {}

  def load_as_bag(self,doc):
        "Creates a bag of words for a single document"
        v = []
        word_freqs = {}
        for w in get_words(file("/home/alibezz/Desktop/Projeto2010/vectors/"+doc).read().split(" ")):
            w = w.lower()
            if not w in word_freqs:
              word_freqs[w] = 1
            else:
              word_freqs[w] += 1
            if not w in self.reverse_map:
                self.reverse_map[w] = self.Nwords
                self.all_words.append(w)
                self.Nwords += 1
            v.append(self.reverse_map[w])
        self.docs.append(v)
        self.docs_freqs.append(word_freqs)

  def pick_label(self):
    return np.random.binomial(1, self.pi)

  def label_documents(self):
    for index,d in enumerate(self.docs):
      label = self.pick_label()
      #FIXME Change if/else to metaprogramming
      self.labels[index] = label
      if label == 0:
        self.c0.append(index)
      else:
        self.c1.append(index)
    print self.labels

  def iterate(self):
    for index,d in enumerate(self.docs):
      #algorithm
 
  def sample(self, nsamples):
    #initialize
    self.pi = random.betavariate(1,1)
    self.label_documents()
    ####
    samples = []
    while len(samples) < nsamples:
      self.iterate()
  
if __name__=='__main__':
  docs = os.listdir(sys.argv[1])
  s = NaiveBayesSampler()
  [s.load_as_bag(x) for x in docs]
  s.sample(10)
