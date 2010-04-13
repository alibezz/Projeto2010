#!/usr/bin/python

#Aline Duarte Bessa - 12/04/10
# This script receives one filename as argument.
# It indicates the source file from where articles will be read.

from BeautifulSoup import BeautifulSoup
import re
import sys

source = open(sys.argv[1], 'r')
line = source.readline()
index = 0; name = sys.argv[1].split('.')
output = open(name[0] + str(index) + '.' + name[1], 'w+')
text = ""

while line:
  line = source.readline()
  if line.rfind("-->", 0, len(line)) >= 0:
    output.write(text)
    output.close()
    index += 1
    output = open(name[0] + str(index) + '.' + name[1], 'w+')
    text = ""
  else:
    text += line

output.write(text)
output.close()
source.close()

