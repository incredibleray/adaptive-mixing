# adaptive-mixing
patent https://patentimages.storage.googleapis.com/32/01/df/bdcbe47a878992/WO2019045798A1.pdf

# thank you, devs and contributors of these libraries!
CABAC: https://github.com/IENT/PyCabac
AE: https://github.com/ahmedfgad/ArithmeticEncodingPython
https://github.com/nayuki/Reference-arithmetic-coding
RLE: https://github.com/tnwei/python-rle
LZ77 and LZ78: https://github.com/biroeniko/lzw-compression
LZW: https://pythonhosted.org/lzw/lzw-module.html

# issue
1. ~LZW and RLE use a different alphabet set.~
2. ~Figure out the length of AE encoded sequence. maybe try this: https://github.com/nayuki/Reference-arithmetic-coding/tree/master/python~
3. ~Use more refined weight, at the moment it is only three digits.~
4. Only need arithmetic encoder, different context, e.g. one uses one previous symbol, the other uses 3 previous symbols.

# overview
use two lossless encoder LZW (Lemple-Ziv) and RLE (Run length) and a entropy encoder AE.

encode the input sequence incrementally, e.g. encode the first letters, then the first two letters, then three, so on and so forth until the entire sequence is encoded.

every encode step, first use LZW and RLE to encode the subsequence, then get the probably table of the LZW and RLE output. 

Mix the probability table, by doing a weighted add of these two tables.

Arithmetical encode both LZW and RLE output with the mixed probability table, then calculate the weight of LZW encoder as rleSequenceLength/(lzwSequenceLength+rleSequenceLength).

# packages
https://github.com/jigar23/CABAC/blob/master/CABAC/src/CABAC.cpp
~https://github.com/FineRedMist/Compression~