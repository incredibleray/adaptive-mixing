import arithmeticcoding
import contextlib, sys
import io
from fractions import Fraction
import math



context1ProbTable=arithmeticcoding.SimpleFrequencyTable([0]*257)

context2ProbTable={}
for i in range(0, 256):
  #for j in range(0, 256):
  #  context2ProbTable[(i, j)]=arithmeticcoding.SimpleFrequencyTable(arithmeticcoding.FlatFrequencyTable(257))
  context2ProbTable[i]=arithmeticcoding.SimpleFrequencyTable([0]*257)
mixedProbTable=arithmeticcoding.SimpleFrequencyTable([0]*257)

probTableTotal=1000000000

def encodedLen(byteArray, adaptive=False):
  # outputCsv=open('details.csv', 'w')
  # outputCsv.write("mixRatio,C1Prob,C2Prob,MixProb\n")

  inp=io.BytesIO()
  inp.write(byteArray)
  inp.seek(0)
  # inp=arithmeticcoding.BitInputStream(inpStream)

  context1Out=io.BytesIO()
  context1Enc = arithmeticcoding.ArithmeticEncoder(32, arithmeticcoding.BitOutputStream(context1Out))

  context2Out=io.BytesIO()
  context2Enc = arithmeticcoding.ArithmeticEncoder(32, arithmeticcoding.BitOutputStream(context2Out))

  mixedOut=io.BytesIO()
  mixedEnc = arithmeticcoding.ArithmeticEncoder(32, arithmeticcoding.BitOutputStream(mixedOut))

  context1=0
  context2=(0, 0)

  trace=[]

  while True:
    symbol = inp.read(1)
    if len(symbol) == 0:
      break

    symbol=symbol[0]

    context1Freq=context1ProbTable
    #context2Freq=context2ProbTable[context2]
    context2Freq=context2ProbTable[context1]
    
    context1Enc.write(context1Freq, symbol)
    context2Enc.write(context2Freq, symbol)

    context1Len=context1Out.tell()
    context2Len=context2Out.tell()

    mixRatio=Fraction(pow(2, context2Len), pow(2, context1Len)+pow(2, context2Len))

    # print("mix ratio={}".format(float(mixRatio)))

    context1Prob=Fraction(context1Freq.get(symbol),context1Freq.get_total())
    context2Prob=Fraction(context2Freq.get(symbol),context2Freq.get_total())
    mixedProb=context1Prob*mixRatio+context2Prob*(1-mixRatio)
    #mixedProb=context2Prob

    assert abs(context2Freq.total-probTableTotal)<5

    #mixedProbNumerator=context2Freq.get(symbol)
    mixedProbNumerator=math.floor(mixedProb*probTableTotal)
    #mixedProbNumerator=math.floor(context1Prob*probTableTotal)
    mixedProbTable.set(symbol, mixedProbNumerator)
    mixedProbTable.set(0, probTableTotal-mixedProbNumerator)

    mixedEnc.write(mixedProbTable, symbol)

    mixedProbTable.set(symbol, 0)

    if adaptive:
      context1Freq.increment(symbol)
      context2Freq.increment(symbol)

    context1=symbol
    context2=(context2[1], symbol)

    trace.append({
      "enc1":context1Out.tell(), 
      "enc2":context2Out.tell(), 
      "mixing":mixedOut.tell(),
      "mixingProb": mixRatio
    })
    # outputCsv.write("{:3f},{:3f},{:3f},{:3f}\n".format(
    #   float(mixRatio), float(context1Prob),float(context2Prob), float(mixedProb)
    # ))

  context1Freq=context1ProbTable
  #context2Freq=context2ProbTable[context2]
  context2Freq=context2ProbTable[context1]

  context1Enc.write(context1Freq, 256)
  context2Enc.write(context2Freq, 256)  # EOF
  mixedEnc.write(context2Freq, 256)

  context1Enc.finish()  # Flush remaining code bits
  context2Enc.finish()
  mixedEnc.finish()

  return context1Out.tell(), context2Out.tell(), mixedOut.tell(), trace, context1Out, context2Out, mixedOut

def bakeContextProbTable(byteArray):
  inp=io.BytesIO()
  inp.write(byteArray)
  inp.seek(0)

  context1=0
  context2=(0, 0)

  while True:
    symbol = inp.read(1)
    if len(symbol) == 0:
      break

    symbol=symbol[0]

    context1Freq=context1ProbTable
    #context2Freq=context2ProbTable[context2]
    context2Freq=context2ProbTable[context1]

    context1Freq.increment(symbol)
    context2Freq.increment(symbol)

    context1=symbol
    context2=(context2[1], symbol)

  context1Freq=context1ProbTable
  #context2Freq=context2ProbTable[context2]
  context2Freq=context2ProbTable[context1]

  context1Freq.increment(256)
  context2Freq.increment(256)

  setContextFreqTablesToSameTotalCount()

def setContextFreqTablesToSameTotalCount():
  for i in range(0, 256):
    #for j in range(0, 256):
    #  table=context2ProbTable[(i,j)]
    table=context2ProbTable[i]

    if table.total == 0:
        continue

    newTable=arithmeticcoding.SimpleFrequencyTable([0]*257)

    for k in range(0, 256):
        newTableCount=math.floor(
        Fraction(probTableTotal*table.get(k),table.get_total()))
        newTable.set(k, newTableCount)

    newTable.set(256, probTableTotal-newTable.total)

    # print("prob table total={}".format(newTable.total))
    # assert newTable.total==probTableTotal
    #context2ProbTable[(i,j)]=newTable
    context2ProbTable[i]=newTable

def decode(byteArray, encoderOut):
    decoderOut=io.BytesIO()
    dec = arithmeticcoding.ArithmeticDecoder(32, arithmeticcoding.BitInputStream(encoderOut))
	
    while True:
        symbol = dec.read(context1ProbTable)
        if symbol == 256:  # EOF symbol
            break
        decoderOut.write(bytes((symbol,)))

    print(decoderOut.read())