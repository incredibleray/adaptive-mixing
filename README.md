# adaptive-mixing
patent https://patentimages.storage.googleapis.com/32/01/df/bdcbe47a878992/WO2019045798A1.pdf

# overview
use two lossless encoder LZW (Lemple-Ziv) and RLE (Run length). a entropy encoder AE, and a mixing module M.

```python
lzwSeq=""
rleSeq=""

lzwOutSeq=""
rleOutSeq=""

foreach (c in inputSeq) {
  lzwSeq+=lzwEncoder.encode(c)
  rleSeq+=xEncoder.encode(c)
  
  lzwProbTable=M.getProbTable(lzwSeq)
  rleProbTable=M.getProbTable(xSeq)
  
  lzwWeight=len(lzwSeq)/(len(lzwSeq)+len(rleSeq))
  
  mixedProbTable=M.mixProbTable(lzwProbTable, rleProbTable, lzwWeight)
  
  lzwOutSeq=AE.encode(lzwSeq, mixedProbTable)
  rleOutSeq=AE.encode(rleSeq, mixedProbTable)
}

if len(lzwOutSeq) < len(rleOutSeq)
  outSeq=lzwOutSeq
else
  outSeq=rleOutSeq
```

# packages
LZW: https://pythonhosted.org/lzw/lzw-module.html
AE: https://github.com/ahmedfgad/ArithmeticEncodingPython
https://github.com/michaeldipperstein/arcode-py
https://github.com/nayuki/Reference-arithmetic-coding
https://pypi.org/project/torchac/
RLE: https://github.com/tnwei/python-rle
