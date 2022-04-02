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

lzwOutSeqLen=0
rleOutSeqLen=0

lzwWeight=0.5

for i in range(1, len(inputSeq)):
  seq=inputSeq[:i]

  lzwSeq=lz.compress(seq)
  rleSeq=rle2.encode_message(seq)

  lzwProbTable=dict(Counter(lzwSeq))
  rleProbTable=dict(Counter(rleSeq))
  
  print("lzw prob\n{}".format(lzwProbTable))
  print("rle prob\n{}".format(rleProbTable))

  weightedProb={}
  for p in lzwProbTable:
    weightedProb[p]=lzwProbTable[p]*lzwWeight

  for p in rleProbTable:
    weightedProb[p]=(weightedProb.get(p) or 0) +rleProbTable[p]*(1-lzwWeight)
  
  # mixedProbTable=M.mixProbTable(lzwProbTable, rleProbTable, lzwWeight)
  print(weightedProb)


# Encode the message
  lzwOutSeq=None
  rleOutSeq=None

  lzwOutSeqLen=ae.encodedLen(lzwSeq, weightedProb)
  rleOutSeqLen=ae.encodedLen(rleSeq, weightedProb)

  print("lzw sequence, len={}".format(lzwOutSeqLen))
  print("rle sequence, len={}".format(rleOutSeqLen))

  lzwWeight=rleOutSeqLen/(lzwOutSeqLen+rleOutSeqLen)

  print("lzw weight={}, rle weight={}".format(lzwWeight, 1-lzwWeight))

  # if len(lzwOutSeq) < len(rleOutSeq):
  #   outSeq=lzwOutSeq
  # else:
  #   outSeq=rleOutSeq

