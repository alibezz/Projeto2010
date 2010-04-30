#Aline Bessa - 30/04/2010
#Text generator to beta version of LSPM

import numpy as np
import random

sp0 = [
[0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
[1, 1, 0, 1, 1, 0, 0, 1, 0, 0],
[1, 1, 1, 0, 1, 0, 1, 0, 0, 0],
[1, 1, 1, 1, 0, 1, 0, 0, 0, 0]]

sp1 = [
[1, 0, 0, 0, 0, 1, 1, 1, 1, 0],
[0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
[0, 0, 1, 0, 0, 1, 1, 0, 1, 1],
[0, 0, 0, 1, 0, 1, 0, 1, 1, 1],
[0, 0, 0, 0, 1, 0, 1, 1, 1, 1]]

def choose_set(label):
    return np.random.binomial(1, abs(label - 0.2))

if __name__=='__main__':
  docs = []
  for i in xrange(10):
    pdoc = np.random.binomial(1, 0.5)
    nsents = random.randint(25, 50)
    doc = []
    for j in xrange(nsents):
      sents_set = choose_set(pdoc)
      if sents_set == 0:
        doc.append(sp0[random.randint(0, 4)])
      else:
        doc.append(sp1[random.randint(0, 4)])
    docs.append(doc)
  print docs       
