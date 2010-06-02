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

  l = ['bl070205ed05pal1', 'bl300804ed32pal1', 'bl160603ed23is2', 'bl291104ed43is2', 'bl140403ed15pal1', 'bl170105ed03pal2', 'bl111102ed41is2', 'bl010702ed24is2', 'bl160804ed30is2', 'bl120503ed18is2', 'bl131104ed41is2', 'bl220304ed11is2', 'bl041102ed40pal2', 'bl031103ed40pal1', 'bl080304ed9pal1', 'bl210604ed22pal1', 'bl061204ed44pal1', 'bl310303ed13pal1', 'bl251102ed43pal1', 'bl080402ed12pal2', 'bl010903ed33pal1', 'bl130502ed17pal1', 'bl210102ed3is2', 'bl170602ed22pal1', 'bl100504ed16is2', 'bl150702ed26pal1', 'bl190503ed19pal2', 'bl090804ed29pal1', 'bl230603ed24pal2', 'bl030105ed01is2', 'bl120802ed30pal1', 'bl080402ed12pal1', 'bl251004ed38pal1', 'bl280703ed28pal1', 'bl261101ed2pal1', 'bl060904ed33pal1', 'bl211002ed38pal1', 'bl110202ed6pal2', 'bl010702ed24pal1', 'bl281002ed39is2', 'bl240504ed18pal1', 'bl021202ed44pal1', 'bl130904ed34pal1', 'bl131204ed45pal1', 'bl290702ed28is2', 'bl101103ed41pal1', 'bl220903ed36pal1', 'bl151203ed45pal1', 'bl290702ed28pal1', 'bl290903ed37pal1', 'bl210703ed27pal2', 'bl240602ed23pal2', 'bl070205ed05is2', 'bl181004ed37is2', 'bl141002ed37pal1', 'bl240504ed18pal2', 'bl031103ed40is2', 'bl290903ed37is2', 'bl280102ed4is2', 'bl140102ed2pal1', 'bl170303ed11pal1', 'bl271003ed39is2', 'bl110302ed9pal2', 'bl140205ed06pal1', 'bl100105ed02pal2', 'bl020902ed33pal2', 'bl171103ed42is2', 'bl220903ed36pal2', 'bl271003ed39pal2', 'bl120104ed2pal2', 'bl140604ed21pal2', 'bl161202ed45pal1', 'bl131204ed45pal2', 'bl050704ed24pal2', 'bl260503ed20pal2', 'bl090603ed22is2', 'bl030504ed15pal1', 'bl200103ed3pal1', 'bl160603ed23pal2', 'bl090902ed34pal1', 'bl030602ed20pal1', 'bl180803ed31pal1', 'bl180302ed10pal1', 'bl270904ed36pal2', 'bl020804ed28pal1', 'bl200502ed18pal1', 'bl081104ed40pal1', 'bl201003ed38pal2', 'bl261101ed2pal2', 'bl290402ed15pal2', 'bl190104ed3is2', 'bl040202ed5pal1', 'bl151203ed45is2', 'bl030105ed01pal2', 'bl011104ed39pal1', 'bl190704ed26pal1', 'bl230804ed31pal1', 'bl230603ed24pal1', 'bl281002ed39pal1', 'bl201204ed46pal1', 'bl080903ed34is2', 'bl260404ed14is2', 'bl120503ed18pal1', 'bl050104ed1pal1', 'bl250302ed11is2', 'bl100203ed6pal1', 'bl071002ed36pal1', 'bl140205ed06is2', 'bl290304ed12is2', 'bl020902ed33pal1', 'bl080702ed25pal1', 'bl171103ed42pal1', 'bl221203ed46is2', 'bl300603ed25pal1', 'bl210102ed3pal1', 'bl131104ed41pal1', 'bl220702ed27pal1', 'bl050802ed29pal2', 'bl260802ed32pal1', 'bl041102ed40pal1', 'bl230204ed7pal1', 'bl280403ed16pal2', 'bl271003ed39pal1', 'bl171103ed42pal2', 'bl070403ed14pal1', 'bl110803ed30pal2', 'bl160603ed23pal1', 'bl190404ed13pal2', 'bl271204ed47is2', 'bl070703ed26is2', 'bl020804ed28pal2', 'bl120802ed30is2', 'bl210604ed22is2', 'bl300804ed32is2', 'bl140604ed21pal1', 'bl260104ed4pal1', 'bl191101ed1is2', 'bl280604ed23pal1', 'bl090603ed22pal1', 'bl070604ed20is2', 'bl170105ed03pal1', 'bl151203ed45pal2', 'bl050802ed29pal1', 'bl220903ed36is2', 'bl080903ed34pal1', 'bl170105ed03is2', 'bl101103ed41pal2', 'bl220702ed27is2', 'bl201003ed38pal1', 'bl160804ed30pal1', 'bl130904ed34is2', 'bl220402ed14is2', 'bl111102ed41pal1', 'bl030303ed9pal1', 'bl110302ed9pal1', 'bl200904ed35is2', 'bl070102ed1pal2', 'bl210703ed27pal1', 'bl150304ed10pal1', 'bl181004ed37pal1', 'bl011203ed43pal2', 'bl200502ed18is2', 'bl070604ed20pal1', 'bl040302ed8pal1', 'bl110803ed30pal1', 'bl290702ed28pal2', 'bl310105ed04is2', 'bl210205ed07is2', 'bl090804ed29is2', 'bl231202ed46pal1', 'bl081203ed44is2', 'bl170602ed22pal2', 'bl030203ed5pal1', 'bl310105ed04pal1', 'bl060502ed16pal1', 'bl030602ed20is2', 'bl170504ed17is2', 'bl070703ed26pal1', 'bl020902ed33is2', 'bl071002ed36pal2', 'bl311201ed5is2', 'bl090204ed5pal1', 'bl210205ed07pal1', 'bl160204ed6pal1', 'bl200904ed35pal1', 'bl101201ed4pal1', 'bl250302ed11pal1', 'bl070102ed1pal1', 'bl140604ed21is2', 'bl280102ed4pal1', 'bl180202ed7pal1', 'bl260404ed14pal1', 'bl240203ed8is2', 'bl180202ed7pal2', 'bl100105ed02pal1', 'bl010903ed33is2', 'bl230804ed31is2', 'bl100602ed21pal1', 'bl311201ed5pal1', 'bl081203ed44pal2', 'bl290304ed12pal1', 'bl270103ed4pal1', 'bl090603ed22pal2', 'bl190104ed3pal1', 'bl220304ed11pal1', 'bl120704ed25pal1', 'bl050704ed24pal1', 'bl190404ed13pal1', 'bl010304ed8pal1', 'bl110803ed30is2', 'bl150903ed35pal1', 'bl250803ed32pal1', 'bl240303ed12pal1', 'bl291104ed43pal1', 'bl190503ed19pal1', 'bl100602ed21is2', 'bl050104ed1pal2', 'bl240602ed23pal1', 'bl050503ed17pal1', 'bl180302ed10is2', 'bl070102ed1is2', 'bl240203ed8pal1', 'bl170203ed7pal1', 'bl031201ed3pal1', 'bl221203ed46pal1', 'bl191101ed1pal1', 'bl271204ed47pal1', 'bl220402ed14pal1', 'bl290402ed15pal1', 'bl011203ed43pal1', 'bl190503ed19is2', 'bl150402ed13pal1', 'bl310303ed13is2', 'bl100303ed10pal1', 'bl130103ed2pal1', 'bl230204ed7is2', 'bl180302ed10pal2', 'bl270502ed19pal1', 'bl251004ed38is2', 'bl110202ed6pal1', 'bl221104ed42pal1', 'bl020603ed21pal1', 'bl270502ed19is2', 'bl081203ed44pal1', 'bl060103ed1pal1', 'bl170504ed17pal1', 'bl231202ed46pal2', 'bl210703ed27is2', 'bl011104ed39pal2', 'bl060103ed1is2', 'bl181102ed42pal1', 'bl300804ed32pal2', 'bl190802ed31pal1', 'bl300902ed35pal1', 'bl090902ed34pal2', 'bl100504ed16pal1', 'bl280403ed16pal1', 'bl260503ed20pal1', 'bl041102ed40is2', 'bl120104ed2pal1', 'bl030105ed01pal1', 'bl310504ed19pal1', 'bl290304ed12pal2']
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
