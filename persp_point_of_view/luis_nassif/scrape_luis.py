#from BeautifulSoup import BeautifulSoup
#import urllib
import sys

html = open(sys.argv[1], "r")
#doc = BeautifulSoup(html)
text = str(html.read())

i = int(sys.argv[2])
#news = len(doc.findAll("p", "by"))

x = text.find('<h2 class="title">')
y = text.find('<div class="service-links">')

while x >= 0 and y >= 0:
  post = text[x:y+len('<div class="service-links">')]
  file = open("file" + str(i), "w+")
  file.write(post)
  file.close()
  text = text.replace(post, "")
  x = text.find('<h2 class="title">')
  y = text.find('<div class="service-links">')
  i += 1
