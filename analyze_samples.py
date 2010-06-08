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

  l = ['bl300603ed25is2', 'bl060103ed1is2', 'bl070604ed20pal2', 'bl260104ed4is2', 'bl211002ed38pal2', 'bl050704ed24pal2', 'bl070403ed14pal2', 'bl050802ed29is2', 'bl090204ed5pal2', 'bl071002ed36is2', 'bl221203ed46pal2', 'bl100203ed6pal2', 'bl251102ed43is2', 'bl010903ed33is2', 'bl151203ed45is2', 'bl081104ed40pal2', 'bl230204ed7pal2', 'bl280403ed16is2', 'bl190104ed3pal2', 'bl300804ed32is2', 'bl170303ed11pal2', 'bl100105ed02is2', 'bl231202ed46is2', 'bl270103ed4is2', 'bl070703ed26pal2', 'bl290702ed28pal2', 'bl081104ed40is2', 'bl010304ed8is2', 'bl090902ed34pal2', 'bl120104ed2is2', 'bl160204ed6pal2', 'bl101201ed4pal2']

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
  for index, fname in enumerate(l):#os.listdir(sys.argv[2])):
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
