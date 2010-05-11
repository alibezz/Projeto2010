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

neut = [
[1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
[0, 0, 1, 1, 0, 0, 0, 0, 1, 0],
[1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
[1, 1, 0, 0, 1, 0, 0, 0, 0, 1],
[0, 0, 0, 1, 1, 0, 0, 1, 0, 0]]

if __name__=='__main__':
  docs = []
  for i in xrange(10):
    persp = np.random.binomial(1, 0.5)
    nsents = random.randint(25, 50)
    doc = []
    for j in xrange(nsents):
     # no_persp = np.random.binomial(1, 0.4)
      #if no_persp:
      # doc.append(neut[random.randint(0, 4)])
      #else:
        if persp == 0:
          doc.append(sp0[random.randint(0, 4)])
        else:
          doc.append(sp1[random.randint(0, 4)])
    docs.append(doc)
  print docs       
