import pyae


def encodedLen(msg, prob_table):
  AE = pyae.ArithmeticEncoding(frequency_table=prob_table,)

  encoded_msg, encoder , interval_min_value, interval_max_value = AE.encode(msg=msg, 
                                                                            probability_table=AE.probability_table)

  print("Encoded Message: {msg}\nMin interval:{min}\nMax interval:{max}\n".format(msg=encoded_msg, min=interval_min_value, max=interval_max_value))
  # Get the binary code out of the floating-point value
  
  i=0
  while int(encoded_msg) != encoded_msg:
    encoded_msg=encoded_msg*2
    i+=1

  return i