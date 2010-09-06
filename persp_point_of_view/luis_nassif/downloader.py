import os

for i in xrange(50):
  os.system("wget http://www.advivo.com.br/categoria/blogs/politica/eleicoes?page=" + str(i + 1)) 
#  os.system(cmd)
#  os.system("mv www.rodrigovianna.com.br pagina" + str(i + 1))
  
