# adaptive-mixing

# overview
use two lossless encoder LZW and X. a entropy encoder AE, and a mixing module M.

lzwSeq=""
xSeq=""

lzwOutSeq=""
xOutSeq=""

foreach (c in inputSeq) {
  lzwSeq+=lzwEncoder.encode(c)
  xSeq+=xEncoder.encode(c)
  
  lzwProbTable=M.getProbTable(lzwSeq)
  xProbTable=M.getProbTable(xSeq)
  
  lzwWeight=len(lzwSeq)/(len(lzwSeq)+len(xSeq))
  
  mixedProbTable=M.mixProbTable(lzwProbTable, xProbTable, lzwWeight)
  
  lzwOutSeq=AE.encode(lzwSeq, mixedProbTable)
  xOutSeq=AE.encode(xSeq, mixedProbTable)
}

if len(lzwOutSeq) < len(xOutSeq)
  outSeq=lzwOutSeq
else
  outSeq=xOutSeq
  
# packages
LZW: https://pythonhosted.org/lzw/lzw-module.html
AE: https://github.com/ahmedfgad/ArithmeticEncodingPython
