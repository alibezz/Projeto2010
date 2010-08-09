import os
import sys

fof = open("labels_oficiais.txt", "r")
fpr = open("labels_bigramas.txt", "r")

dif0 = dif1 = eql0 = eql1 = 0.0

lof = fof.readline()
lpr = fpr.readline()

while(lof != "" and lpr != ""):
  if (lof == "0\n" and lpr == "1\n"):
    dif0 += 1.0
  elif (lof == "0\n" and lpr == "0\n"): 
   eql0 += 1.0
  elif (lof == "1\n" and lpr == "0\n"):
   dif1 += 1.0
  else:
   eql1 += 1.0

  lof = fof.readline()
  lpr = fpr.readline()

fof.close()
fpr.close()

pr0 = eql0/(eql0 + dif0)
pr1 = eql1/(eql1 + dif1)
rec0 = eql0/(eql0 + dif1)
#rec1 = eql1/(eql1 + dif0)
print "precision (class 0): " + str(pr0)
print "precision (class 1): " + str(pr1)
print "recall (class 0): " + str(rec0)
#print "recall (class 1): " + str(rec1)
print "accuracy: " + str((eql0 + eql1)/(eql0 + eql1 + dif0 + dif1))
print "F-measure (class 0): " + str((2*pr0*rec0)/(rec0 + pr0))
#print "F-measure (class 1): " + str((2*pr1*rec1)/(rec1 + pr1))
