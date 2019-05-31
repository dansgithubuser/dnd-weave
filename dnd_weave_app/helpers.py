import weave

import math

def plaintext_to_jsonable(plaintext):
    d = weave.plaintext_to_dict(plaintext)
    for k in d.keys():
        if d[k] == math.inf:
            d[k] = 'infinity'
    return d

def decrypt(spell, character):
    secret = weave.Secret().deserialize(character.secret.serialized)
    try:
        ciphertext = weave.runes_to_ciphertext(spell.runes.split(), secret)
    except:
        return {'error': 'invalid runes'}
    plaintext = weave.ciphertext_to_plaintext(ciphertext, secret)
    return plaintext_to_jsonable(plaintext)
