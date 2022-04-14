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

for i in range(2000, len(inputSeq), 500):
  seq=inputSeq[:i]

  # print("input sequence\n{}".format(seq))
  print("input sequence len={}".format(i))
  # lzwSeq=lz.compress(seq)
  # rleSeq=rle2.encode_message(seq)
  lzwSeq, _, _=lz77.encode_lz77(seq, 128, 12)
  rleSeq, _, _=lz77.encode_lz77(seq, 250, 24)
  print("lzw_128_7 encoded sequence len={}".format(len(lzwSeq)))
  print("lzw_250_8 encoded sequence len={}".format(len(rleSeq)))

  lzwProbTable=dict(Counter(lzwSeq))
  rleProbTable=dict(Counter(rleSeq))
  
  print("lzw_128_7 probability table")
  # probabilityTable.printTable(lzwProbTable)

  print("lzw_250_8 probability table")
  # probabilityTable.printTable(rleProbTable)


  lzwAeSeqLen=ae.encodedLen(lzwSeq, lzwProbTable)
  print("lzw_128_7 own probability encoded length={}".format(lzwAeSeqLen))

  rleAeSeqLen=ae.encodedLen(rleSeq, rleProbTable)
  print("lzw_250_8 own probability encoded length={}".format(rleAeSeqLen))

  lzwWeight=int(1000*rleAeSeqLen/(lzwAeSeqLen+rleAeSeqLen))

  print("lzw_128_7 weight={:1.3f}, lzw_250_8 weight={:1.3f}".format(lzwWeight/1000, 1-lzwWeight/1000))

  weightedProb={}
  for p in lzwProbTable:
    weightedProb[p]=lzwProbTable[p]*lzwWeight

  for p in rleProbTable:
    weightedProb[p]=(weightedProb.get(p) or 0) +rleProbTable[p]*(1000-lzwWeight)
  
  # mixedProbTable=M.mixProbTable(lzwProbTable, rleProbTable, lzwWeight)
  print("mixed probability table")
  # probabilityTable.printTable(weightedProb)
  probabilityTable.printentropy(weightedProb)

# Encode the message
  lzwOutSeq=None
  rleOutSeq=None

  lzwOutSeqLen=ae.encodedLen(lzwSeq, weightedProb)
  rleOutSeqLen=ae.encodedLen(rleSeq, weightedProb)

  print("lzw_128_7 mixed probability encoded length={}".format(lzwOutSeqLen))
  print("lzw_250_8 mixed probability encoded length={}".format(rleOutSeqLen))

  # if len(lzwOutSeq) < len(rleOutSeq):
  #   outSeq=lzwOutSeq
  # else:
  #   outSeq=rleOutSeq
