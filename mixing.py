import rle2 
import lz
import ae
from collections import Counter
import lz77
import probabilityTable

# binascii.rlecode_hqx
# inputSeq="TTTTTT555555oooopppppppppp"
inputSeq=open('text.txt', 'r').read()

lzwSeq=""
rleSeq=""

lzwOutSeq=""
rleOutSeq=""

lzwOutSeqLen=0
rleOutSeqLen=0

lzwWeight=500

for i in range(20, len(inputSeq), 20):
  seq=inputSeq[:i]

  print("input sequence\n{}".format(seq))
  # lzwSeq=lz.compress(seq)
  # rleSeq=rle2.encode_message(seq)
  lzwSeq, _, _=lz77.encode_lz77(seq, 8, 3)
  rleSeq, _, _=lz77.encode_lz77(seq, 49, 7)
  print("lzw_8_3 encoded sequence\n{}".format(lzwSeq))

  lzwProbTable=dict(Counter(lzwSeq))
  rleProbTable=dict(Counter(rleSeq))
  
  print("lzw_8_3 probability table")
  probabilityTable.printTable(lzwProbTable)
  print("lzw_49_7 probability table")
  probabilityTable.printTable(rleProbTable)

  weightedProb={}
  for p in lzwProbTable:
    weightedProb[p]=lzwProbTable[p]*lzwWeight

  for p in rleProbTable:
    weightedProb[p]=(weightedProb.get(p) or 0) +rleProbTable[p]*(1000-lzwWeight)
  
  # mixedProbTable=M.mixProbTable(lzwProbTable, rleProbTable, lzwWeight)
  print("weighted probability table")
  probabilityTable.printTable(weightedProb)

# Encode the message
  lzwOutSeq=None
  rleOutSeq=None

  lzwOutSeqLen=ae.encodedLen(lzwSeq, weightedProb)
  rleOutSeqLen=ae.encodedLen(rleSeq, weightedProb)

  print("lzw_8_3 mixed probability encoded length={}".format(lzwOutSeqLen))
  print("lzw_49_7 mixed probability encoded length={}".format(rleOutSeqLen))

  lzwWeight=int(1000*rleOutSeqLen/(lzwOutSeqLen+rleOutSeqLen))

  print("lzw_8_3 weight={:1.3f}, lzw_49_7 weight={:1.3f}".format(lzwWeight/1000, 1-lzwWeight/1000))

  # if len(lzwOutSeq) < len(rleOutSeq):
  #   outSeq=lzwOutSeq
  # else:
  #   outSeq=rleOutSeq
