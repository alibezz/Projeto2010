import os

for i in xrange(4):
  cmd = "wget http://veja.abril.com.br/blog/mainardi/page/" + str(i + 1) + "/"
  os.system(cmd)
  
