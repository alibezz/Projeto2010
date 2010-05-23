#Aline Bessa - 23/05/2010
#This program intends to keep track of which documents were written by each of the authors - and under which viewpoint.
#SPECIALIZED TO BITTERLEMONS ORIGINAL CORPUS

import os
import sys

def author_name(string):
  ind = string.find("with")
  if ind >= 0:
    return string[ind + 5:]
  else:
    return string

if __name__=='__main__':
  meta_dir = os.listdir(sys.argv[1])
  relation = {}; view = ""
  
  for file in meta_dir:
    for ind, line in enumerate(open(os.path.realpath(sys.argv[1] + '/' + file), 'r')):
      columns = line.split("\t")
      if columns[3] == "meta_viewpoint":
        view = columns[4].strip("\n")
      elif columns[3] == "meta_author":
        author = author_name(columns[4]).strip("\n")
        if not author in relation:
          relation[author] = [[file, view]] 
        else:
          relation[author].append([file, view])

  print relation 
     

 
