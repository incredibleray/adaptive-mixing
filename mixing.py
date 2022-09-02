
import ae
from collections import Counter
import probabilityTable
import pyae


# binascii.rlecode_hqx
# inputSeq="TTTTTT555555oooopppppppppp"
inputSeq=open('text.txt', 'r').read(100000)
outputCsv=open('out.csv', 'w')

lzwSeq=""
rleSeq=""

lzwOutSeq=""
rleOutSeq=""

lzwOutSeqLen=0
rleOutSeqLen=0

lzwWeight=500

outputCsv.write("inputLength, context 1 Encoded Length, context 2 Encoded Length, Mixing encoded length\n")

print("input sequence len={}".format(len(inputSeq)))
ae.bakeContextProbTable(inputSeq.encode('utf-8'))

# for i in range(2000, len(inputSeq), 500):
for i in range(10, 300, 10):
  seq=inputSeq[:i]

  # print("input sequence\n{}".format(seq))
  print("input sequence len={}".format(i))

  byteArray=seq.encode('utf-8')

  outLen1, outLen2, outLen3, trace=ae.encodedLen(byteArray, False)

  print("encoded message len 1={}, 2={}, 3={}".format(outLen1, outLen2, outLen3))

  threeQuarterIndex=int(len(trace)*3/4)
  lastQuarterLen1=outLen1-trace[threeQuarterIndex]["enc1"]
  lastQuarterLen2=outLen2-trace[threeQuarterIndex]["enc2"]
  lastQuarterLen3=outLen3-trace[threeQuarterIndex]["mixing"]

  print("encoded message of last quarter len 1={}, 2={}, 3={}, last quarter point mixing prob={}".format(lastQuarterLen1, lastQuarterLen2, lastQuarterLen3, float(trace[lastQuarterLen3]["mixingProb"])))
  
  outputCsv.write("{},{},{},{}\n".format(i,outLen1, outLen2, outLen3))
  
  #outputCsv.write("{},{},{},{},{},{},{}\n".format(i,outLen1, outLen2, outLen3, lastQuarterLen1, lastQuarterLen2, lastQuarterLen3))
  # rleAeSeqLen=ae.encodedLen(rleSeq, rleProbTable)
  # print("lzw_250_8 own probability encoded length={}".format(rleAeSeqLen))

  # lzwWeight=int(1000*rleAeSeqLen/(lzwAeSeqLen+rleAeSeqLen))

  # print("lzw_128_7 weight={:1.3f}, lzw_250_8 weight={:1.3f}".format(lzwWeight/1000, 1-lzwWeight/1000))

  # weightedProb={}
  # for p in lzwProbTable:
  #   weightedProb[p]=lzwProbTable[p]*lzwWeight

  # for p in rleProbTable:
  #   weightedProb[p]=(weightedProb.get(p) or 0) +rleProbTable[p]*(1000-lzwWeight)
  
  # # mixedProbTable=M.mixProbTable(lzwProbTable, rleProbTable, lzwWeight)
  # print("mixed probability table")
  # # probabilityTable.printTable(weightedProb)
  # probabilityTable.printentropy(weightedProb)
outputCsv.close()
# # Encode the message
#   lzwOutSeq=None
#   rleOutSeq=None

#   lzwOutSeqLen=ae.encodedLen(lzwSeq, weightedProb)
#   rleOutSeqLen=ae.encodedLen(rleSeq, weightedProb)

#   print("lzw_128_7 mixed probability encoded length={}".format(lzwOutSeqLen))
#   print("lzw_250_8 mixed probability encoded length={}".format(rleOutSeqLen))

  # if len(lzwOutSeq) < len(rleOutSeq):
  #   outSeq=lzwOutSeq
  # else:
  #   outSeq=rleOutSeq
