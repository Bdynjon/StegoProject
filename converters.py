import numpy as np


def text_to_bits(text, encoding="utf-8", errors="surrogatepass"):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def encode_string(string: str):
    array = []

    for sign in string:
        sign_code = text_to_bits(sign)

        for o in sign_code:
            array.append(np.uint8(o))

    n_array = np.array(array)
    return n_array


def decode_string(array):
    bits_string = ""

    for sign in array:
        bits_string += str(sign)

    text = ""

    for i in range(8, len(bits_string)+8, 8):
        try:
            text += text_from_bits(bits_string[i-8:i])
        except:
            break

    return text