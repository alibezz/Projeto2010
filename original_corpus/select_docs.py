#Aline Bessa - 23/05/2010
#This program intends to keep track of which documents were written by each of the authors - and under which viewpoint.
#SPECIALIZED TO BITTERLEMONS ORIGINAL CORPUS

import os
import sys
import math
import random

class SelectDocs(object):
  def __init__(self, dir, corpus):
    self.dir = dir
    self.corpus = corpus
    self.relation = {}

  def author_name(self, string):
    ind = string.find("with")
    if ind >= 0:
      return string[ind + 5:]
    else:
      return string

  def generate_relations(self):
    view = ""
    for file in self.corpus:
      for ind, line in enumerate(open(os.path.realpath(self.dir + '/' + file), 'r')):
        columns = line.split("\t")
        if columns[3] == "meta_viewpoint":
          view = columns[4].strip("\n")
        elif columns[3] == "meta_author":
          author = self.author_name(columns[4]).strip("\n")
          if not author in self.relation:
            self.relation[author] = [[file, view]] 
          else:
            self.relation[author].append([file, view])

  def pretty_print(self):
    "prints relation in a human-readable way"

  def pick_docs(self, percentage):
    "picks a percentage of authors and, as a consequence, all their docs"
    num_authors = int(math.ceil(len(self.relation.keys()) * percentage))
    temp = self.relation.keys()
    authors = []

    for i in xrange(num_authors):
      index = random.randint(0, len(temp) - 1)
      authors.append(temp[index])
      del temp[index] 

    selected_docs = []
    for index, name in enumerate(authors):
      for i in xrange(len(self.relation[name])):
        selected_docs.append(self.relation[name][i][0])
    
    return selected_docs     

if __name__=='__main__':
  a = SelectDocs(sys.argv[1], os.listdir(sys.argv[1]))
  a.generate_relations()
  print a.pick_docs(0.4)
