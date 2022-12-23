# adaptive-mixing
patent https://patentimages.storage.googleapis.com/32/01/df/bdcbe47a878992/WO2019045798A1.pdf

# AV1 experiment

## tech docs
https://aomedia.org/docs/AV1_ToolDescription_v11-clean.pdf

https://arxiv.org/pdf/2008.06091.pdf

## contexts in av1 description
The context model applied to the lower-level plane depends on 1) the primary transform directions,
namely: bi-directional, horizontal, and vertical; 2) the transform block size; and 3) up to five
neighbouring transform coefficients in the transform domain. The middle-level plane uses a similar
context model, but the number of context neighbour coefficients is reduced from 5 to 2. The
higher-level plane is coded by Exp-Golomb code without using context modelling. For the sign
plane, with the exception of the DC sign, which is coded using the DC signs from neighbouring
transform units, sign values of all other coefficients are coded directly without context modelling.

## plan
change arithmetic coding for one plane first, lower-level or mid-level.


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
4. ~Only need arithmetic encoder, different context, e.g. one uses one previous symbol, the other uses 3 previous symbols.~
5. need to find a airthmetic encoder that supports multiple probablity tables, or a cabac that supports mixing probablity. 
6. listing some libraries to investigate:
https://github.com/jigar23/CABAC/tree/master/CABAC/src
* https://github.com/dmitrykravchenko2018/arithmetic_coding
https://github.com/WaleedYaser/Arithmetic-Coding/blob/41fb8c27062870973e5c6c2bca4e6f387867436c/Arithmatic.py#L26
https://github.com/fab-jul/torchac/blob/master/torchac/backend/torchac_backend.cpp
https://github.com/scresh/arithmetic_coding/blob/master/coding/encoder.py

# overview
use two lossless encoder LZW (Lemple-Ziv) and RLE (Run length) and a entropy encoder AE.

encode the input sequence incrementally, e.g. encode the first letters, then the first two letters, then three, so on and so forth until the entire sequence is encoded.

every encode step, first use LZW and RLE to encode the subsequence, then get the probably table of the LZW and RLE output. 

Mix the probability table, by doing a weighted add of these two tables.

Arithmetical encode both LZW and RLE output with the mixed probability table, then calculate the weight of LZW encoder as rleSequenceLength/(lzwSequenceLength+rleSequenceLength).

# packages
https://github.com/jigar23/CABAC/blob/master/CABAC/src/CABAC.cpp
~https://github.com/FineRedMist/Compression~
