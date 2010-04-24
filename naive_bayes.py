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

  def remove_document(self, doc_index):
    wclass = self.labels[doc_index]
    #FIXME Change if/else to metaprogramming
    if wclass == 0:
      self.c0.remove(doc_index)
      self.Nc0 -= 1
    else:    
      self.c1.remove(doc_index)
      self.Nc1 -= 1
  
  def makebag(self, i):
    bag = []
    for word in self.all_words:
      bag.append(self.docs[i][word])
    return bag  

  def word_in_class_frequency(self, wclass, word):
    word_count = 0
    for index in wclass:
       word_count += self.docs_freqs[index][word]
    return word_count

  def sum_word_freqs(self, wclass):
    freq_sum = 0
    for word in self.all_words:
      freq_sum += self.word_in_class_frequency(wclass, word)
    return freq_sum

  def class_prob(self, wclass):
    product = 1.0
    for word in self.all_words:
      product *= (self.word_in_class_frequency(wclass, word) + 1.0) / (self.sum_word_freqs(wclass) + 1.0)
     
    #FIXME Change len(wclass) to metaprogramming on c_i
    return ((len(wclass) + 1.0) / (self.Nwords + 1.0)) * product

  def sample_label(self):
    value0 = self.class_prob(self.c0)
    value1 = self.class_prob(self.c1)
    new_pi = value1 / (value0 + value1)
    return np.random.binomial(1, new_pi)

  def classify_document(self, index, new_label):
    #FIXME Change if/else to metaprogramming
    if new_label == 0:
      self.c0.append(index)
      self.Nc0 += 1
    else:
      self.c1.append(index)
      self.Nc1 += 1
    self.labels[index] = new_label

  def iterate(self):
    for index in range(len(self.docs)):
      #considering a non-supervised environment
      self.remove_document(index)
      new_label = self.sample_label()
      self.classify_document(index, new_label)
    return self.labels.copy()

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
   

   # samples = []
   # 
   # while len(samples) < nsamples:
   #   it = self.iterate()
   #   samples.append(it)
   #   if len(samples) % 10 == 0:
   #     print it
   #     print '\n'

if __name__=='__main__':
  docs = os.listdir(sys.argv[1])
  s = NaiveBayesSampler()
  [s.load_as_bag(x) for x in docs]
  print s.sample(1000)
