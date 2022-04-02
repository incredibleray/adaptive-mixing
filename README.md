# adaptive-mixing
patent https://patentimages.storage.googleapis.com/32/01/df/bdcbe47a878992/WO2019045798A1.pdf

# issue
1. LZW and RLE use a different alphabet set.

# overview
use two lossless encoder LZW (Lemple-Ziv) and RLE (Run length). a entropy encoder AE, and a mixing module M.

encode the input sequence incrementally, e.g. encode the first letters, then the first two letters, then three, so on and so forth until the entire sequence is encoded.

every encode step, first use LZW and RLE to encode the subsequence, then get the probably table of the LZW and RLE output. 

Mix the probability table, by doing a weighted add of these two tables.

Arithmetical encode both LZW and RLE output with the mixed probability table, then calculate the weight of LZW encoder as rleSequenceLength/(lzwSequenceLength+rleSequenceLength).

# packages
LZW: https://pythonhosted.org/lzw/lzw-module.html
AE: https://github.com/ahmedfgad/ArithmeticEncodingPython
https://github.com/michaeldipperstein/arcode-py
https://github.com/nayuki/Reference-arithmetic-coding
https://pypi.org/project/torchac/
RLE: https://github.com/tnwei/python-rle
