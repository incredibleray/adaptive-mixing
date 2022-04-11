import arithmeticcoding
import contextlib, sys
import io

def encodedLen(msg, prob_table):
  inp=io.BytesIO()
  inp.write(bytes(msg))
  inp.seek(0)
  # inp=arithmeticcoding.BitInputStream(inpStream)
  freqs=get_frequencies(prob_table)
  outStream=io.BytesIO()
  bitout=arithmeticcoding.BitOutputStream(outStream)

  enc = arithmeticcoding.ArithmeticEncoder(32, bitout)
  while True:
    symbol = inp.read(1)
    if len(symbol) == 0:
      break
    enc.write(freqs, symbol[0])
  enc.write(freqs, 256)  # EOF
  enc.finish()  # Flush remaining code bits

  outStream.seek(0)
  return len(outStream.read())

# Returns a frequency table based on the bytes in the given file.
# Also contains an extra entry for symbol 256, whose frequency is set to 0.
def get_frequencies(prob_table):
  freqs = arithmeticcoding.SimpleFrequencyTable([0] * 257)
  for (k,v) in prob_table.items():
    freqs.set(k, int(v))

  freqs.increment(256)
  return freqs