import math

def printTable(table):
  total=sum(table.values())
  tableOut=""
  for k, v in table.items():
    tableOut+="{}:{:1.3f},\t".format(k, v/total)

  print(tableOut)

def printentropy(table):
  total=sum(table.values())
  entropy=0
  for k, v in table.items():
    entropy+=-math.log2(v/total)

  print("entropy is {:.2f}".format(entropy))