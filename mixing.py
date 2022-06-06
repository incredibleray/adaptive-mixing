
import ae
from collections import Counter
import probabilityTable
import pyae


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

# for i in range(2000, len(inputSeq), 500):
for i in range(2000, 2001, 500):
  seq=inputSeq[:i]

  # print("input sequence\n{}".format(seq))
  print("input sequence len={}".format(i))

  probTable=dict(Counter(seq))
  
  ae=pyae.ArithmeticEncoding(probTable)

  encoded_msg, encoder, interval_min_value, interval_max_value=ae.encode(seq, ae.probability_table)
  
  print("encoded message={}\nmin={}\nmax={}".format(encoded_msg, interval_min_value, interval_max_value))

  binary_code, binary_encoder=ae.encode_binary(interval_min_value,interval_max_value)
  print("binary code={}".format(binary_code))
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
