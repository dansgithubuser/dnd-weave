import weave

import math

def plaintext_to_jsonable(plaintext):
    d = weave.plaintext_to_dict(plaintext)
    for k in d.keys():
        if d[k] == math.inf:
            d[k] = 'infinity'
    return d
