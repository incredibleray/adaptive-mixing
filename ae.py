import arithmeticcoding
import contextlib, sys
import io

context1ProbTable={}
for i in range(0, 256):
  context1ProbTable[i]=arithmeticcoding.SimpleFrequencyTable(arithmeticcoding.FlatFrequencyTable(257))

context2ProbTable={}
for i in range(0, 256):
  for j in range(0, 256):
    for k in range(0, 256):
      context2ProbTable[(i, j, k)]=arithmeticcoding.SimpleFrequencyTable(arithmeticcoding.FlatFrequencyTable(257))

mixedProbTable=arithmeticcoding.SimpleFrequencyTable([0] * 257)

def encodedLen(byteArray):
  inp=io.BytesIO()
  inp.write(byteArray)
  inp.seek(0)
  # inp=arithmeticcoding.BitInputStream(inpStream)

  context1Out=io.BytesIO()
  context1Enc = arithmeticcoding.ArithmeticEncoder(32, arithmeticcoding.BitOutputStream(context1Out))

  context2Out=io.BytesIO()
  context2Enc = arithmeticcoding.ArithmeticEncoder(32, arithmeticcoding.BitOutputStream(context2Out))

  context1=0
  context2=(0, 0, 0)

  while True:
    symbol = inp.read(1)
    if len(symbol) == 0:
      break

    symbol=symbol[0]

    context1Freq=context1ProbTable[context1]
    context2Freq=context2ProbTable[context2]
    
    context1Enc.write(context1Freq, symbol)
    context2Enc.write(context2Freq, symbol)

    context1Freq.increment(symbol)
    context2Freq.increment(symbol)

    context1Len=context1Out.tell()
    context2Len=context2Out.tell()

    context1=symbol
    context2=(context2[1], context2[2], symbol)

  context1Freq=context1ProbTable[context1]
  context2Freq=context2ProbTable[context2]

  context1Enc.write(context1Freq, 256)
  context2Enc.write(context2Freq, 256)  # EOF
  
  context1Enc.finish()  # Flush remaining code bits
  context2Enc.finish()

  return context1Out.tell(), context2Out.tell()

# Returns a frequency table based on the bytes in the given file.
# Also contains an extra entry for symbol 256, whose frequency is set to 0.
def get_frequencies(prob_table):
  freqs = arithmeticcoding.SimpleFrequencyTable([0] * 257)
  for (k,v) in prob_table.items():
    freqs.set(k, int(v))

  freqs.increment(256)
  return freqs

#   import contextlib, sys
# import arithmeticcoding


# # Command line main application function.
# def main(args):
# 	# Handle command line arguments
# 	if len(args) != 2:
# 		sys.exit("Usage: python adaptive-arithmetic-compress.py InputFile OutputFile")
# 	inputfile, outputfile = args
	
# 	# Perform file compression
# 	with open(inputfile, "rb") as inp, \
# 			contextlib.closing(arithmeticcoding.BitOutputStream(open(outputfile, "wb"))) as bitout:
# 		compress(inp, bitout)


# def compress(inp, bitout):
# 	initfreqs = arithmeticcoding.FlatFrequencyTable(257)
# 	freqs = arithmeticcoding.SimpleFrequencyTable(initfreqs)
# 	enc = arithmeticcoding.ArithmeticEncoder(32, bitout)
# 	while True:
# 		# Read and encode one byte
# 		symbol = inp.read(1)
# 		if len(symbol) == 0:
# 			break
# 		enc.write(freqs, symbol[0])
# 		freqs.increment(symbol[0])
# 	enc.write(freqs, 256)  # EOF
# 	enc.finish()  # Flush remaining code bits


# # Main launcher
# if __name__ == "__main__":
# 	main(sys.argv[1 : ])