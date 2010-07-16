import os

for i in xrange(5):
  cmd = "wget http://veja.abril.com.br/blog/augusto-nunes/secao/feira-livre/page/" + str(i + 1) + "/"
  os.system(cmd)
  
