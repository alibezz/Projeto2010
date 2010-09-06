import os

j = 20
for i in xrange(35):
  os.system("python scrape_luis.py ../eleicoes\?page\=" + str(i + 16) + " " + str(280 + j))
  j += 20

