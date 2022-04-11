def printTable(table):
  total=sum(table.values())
  tableOut=""
  for k, v in table.items():
    tableOut+="{}:{:1.3f},\t".format(k, v/total)

  print(tableOut)
