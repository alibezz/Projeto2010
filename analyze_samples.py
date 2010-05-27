#Aline Bessa - 26/05/2010
#This program analyses some properties in samples written in a file
#It considers that the indexes in the array correspond to files order
# in the directory
#ARGS: sys.argv[1] - File with samples
#      sys.argv[2] - Directory containing files related to samples

import os
import sys
import numpy

if __name__=='__main__':

  sfile = open(sys.argv[1], 'r')
  samples = []

  for line in sfile:
    line = line.lstrip('[')
    line = line.rstrip(']\n')
    sample = [int(x) for x in line.split(',')]
    samples.append(numpy.array(sample))

  sfile.close()

  #Assume (arbitrary) that isr == 0 and pal == 1
  persps = []; cisr = 0; cpal = 0
  for index, fname in enumerate(os.listdir(sys.argv[2])):
    if fname.find("is") >= 0:
       cisr += 1
       persps.append(0)
    else:
       cpal += 1
       persps.append(1)

  persps = numpy.array(persps) 

  print "Error rate considering isr == 0 and pal == 1"
  
  for i in xrange(len(samples)):
    print numpy.sum(numpy.abs(persps - samples[i]))/float(len(persps))
