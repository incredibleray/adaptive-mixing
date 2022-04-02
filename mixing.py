import rle2 
import lz
import ae
from collections import Counter

# binascii.rlecode_hqx
inputSeq="TTTTTT555555oooopppppppppp"

lzwSeq=""
rleSeq=""

lzwOutSeq=""
rleOutSeq=""

for i in range(1, len(inputSeq)):
  seq=inputSeq[:i]

  lzwSeq=lz.compress(seq)
  rleSeq=rle2.encode_message(seq)

  lzwProbTable=dict(Counter(lzwSeq))
  rleProbTable=dict(Counter(rleSeq))
  
  print("lzw prob\n{}".format(lzwProbTable))
  print("rle prob\n{}".format(rleProbTable))

  lzwAe=ae.encodedLen(lzwSeq, lzwProbTable)
  rleAe=ae.encodedLen(rleSeq, rleProbTable)

  print("lzw AE:"+str(lzwAe))
  print("rle AE:"+str(rleAe))
  
  lzwWeight=lzwAe/(lzwAe+rleAe)
  
  weightedProb={}
  for p in lzwProbTable:
    weightedProb[p]=lzwProbTable[p]*lzwWeight

  for p in rleProbTable:
    weightedProb[p]=(weightedProb.get(p) or 0) +rleProbTable[p]*(1-lzwWeight)
  
  # mixedProbTable=M.mixProbTable(lzwProbTable, rleProbTable, lzwWeight)
  print(weightedProb)


# Encode the message
  lzwOutSeq=ae.encodedLen(lzwSeq, weightedProb)
  rleOutSeq=ae.encodedLen(rleSeq, weightedProb)

  print("lzw sequence, len={}".format(lzwOutSeq))
  print("rle sequence, len={}".format(rleOutSeq))

  # if len(lzwOutSeq) < len(rleOutSeq):
  #   outSeq=lzwOutSeq
  # else:
  #   outSeq=rleOutSeq

