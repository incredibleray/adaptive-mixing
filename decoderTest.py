
from pickle import BYTEARRAY8
import ae
from collections import Counter
import probabilityTable
import pyae
import arithmeticcoding
import contextlib, sys
import io

# binascii.rlecode_hqx
# inputSeq="TTTTTT555555oooopppppppppp"
i=10
inputSeq=open('text.txt', 'r').read(i)
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

seq=inputSeq

  # print("input sequence\n{}".format(seq))
print("input sequence len={}".format(i))

byteArray=seq.encode('utf-8')
inp=io.BytesIO()
inp.write(byteArray)
inp.seek(0)
context1Out=io.BytesIO()
context1Enc = arithmeticcoding.ArithmeticEncoder(32, arithmeticcoding.BitOutputStream(context1Out))

while True:
    symbol = inp.read(1)
    if len(symbol) == 0:
        break

    symbol=symbol[0]

    context1Freq=ae.context1ProbTable
    context1Enc.write(context1Freq, symbol)
context1Freq=ae.context1ProbTable

context1Enc.write(context1Freq, 256)

context1Enc.finish()  # Flush remaining code bits

decoderOut=io.BytesIO()
dec = arithmeticcoding.ArithmeticDecoder(32, arithmeticcoding.BitInputStream(context1Out))
	
while True:
    symbol = dec.read(ae.context1ProbTable)
    if symbol == 256:  # EOF symbol
        break
    decoderOut.write(bytes((symbol,)))

print(decoderOut.read())

