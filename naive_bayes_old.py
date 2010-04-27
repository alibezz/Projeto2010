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
    self.c0 = []
    self.c1 = []
    self.Nc0 = 0
    self.Nc1 = 0

    self.labels = {} 
    self.docs = []
    self.bags = []
 
    self.all_words = []
    self.Nwords = 0
    self.docs_freqs = []
    self.reverse_map = {}

  def makebag(self, i):
    bag = []
    for word in self.all_words:
      if word in self.docs[i]:
        bag.append(self.docs[i][word])
      else:
        bag.append(0)
    return bag


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

    self.Nc0 = len(self.c0)
    self.Nc1 = len(self.c1)

  def remove_document(self, doc_index):
    wclass = self.labels[doc_index]
    #FIXME Change if/else to metaprogramming
    if wclass == 0:
      self.c0.remove(doc_index)
      self.Nc0 -= 1
    else:    
      self.c1.remove(doc_index)
      self.Nc1 -= 1

  def word_in_class_frequency(self, wclass, word):
    word_count = 0
    for index in wclass:
       word_count += self.docs_freqs[index][word]
    return word_count

  def sum_word_freqs(self, wclass, index):
    freq_sum = 0
    vector = self.bags[index]
    for i in xrange(len(self.all_words)):
      freq_sum += vector[i]
    return freq_sum

  def class_prob(self, wclass, index):
    product = 1.0
    for word in self.all_words:
      product *= (self.word_in_class_frequency(wclass, word) + 1.0) / (self.sum_word_freqs(wclass, index) + 1.0)
     
    #FIXME Change len(wclass) to metaprogramming on c_i
    return ((len(wclass) + 1.0) / (self.Nwords + 1.0)) * product 

  def sample_label(self, index):
    value0 = self.class_prob(self.c0, index)
    value1 = self.class_prob(self.c1, index)
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
      new_label = self.sample_label(index)
      self.classify_document(index, new_label)
    return self.labels.copy()

  def sample(self, nsamples):
    #initialize
    self.pi = random.betavariate(1,1)
    self.label_documents()
    for i in xrange(len(self.labels)):
      self.bags.append(self.makebag(i))

    ####
    samples = []
    
    while len(samples) < nsamples:
      it = self.iterate()
      samples.append(it)
      print it

if __name__=='__main__':
  docs = os.listdir(sys.argv[1])
  s = NaiveBayesSampler()
  [s.load_as_bag(x) for x in docs]
  s.sample(10)
