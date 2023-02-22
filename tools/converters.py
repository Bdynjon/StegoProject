import numpy as np
from functools import reduce


def text_to_bits(text, encoding="utf-8", errors="surrogatepass"):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def encode_string(string: str):
    array = map(text_to_bits, string)
    array = list(reduce(lambda res, el: res+el, array))
    size = len(array)
    size_code = list(bin(size)[2:].zfill(15))

    return size_code + array


def decode_string(array):
    size_text = "".join(array[:15])
    size = int("0b" + size_text[::-1], 2)

    bits_string = "".join(array[15:])
    text = ""
    for i in range(8, size+8, 8):
        try:
            text += text_from_bits(bits_string[i-8:i])
        except:
            continue

    return text


def encode_image(image):
    size = image.shape
    array = []
    size_arr = bin(size[0])[2:].zfill(12) + bin(size[1])[2:].zfill(12)
    image = np.uint8(image / 255)

    for bit in size_arr:
        array.append(np.uint8(bit))

    for st in image:
        for el in st:
            array.append(el)

    return array


def decode_image(array):
    size_string = ""
    for i in range(24):
        size_string += str(array[i])

    size = (int("0b"+size_string[:12], 2), int("0b"+size_string[12:24], 2))

    image = np.zeros(size, dtype=np.uint8)

    for i in range(size[0]):
        for j in range(size[1]):
            image[i, j] = array[j + i*size[1] + 24] * 255

    return image


if __name__ == "__main__":
    test_message = "Text message"

    a = text_to_bits('Е')
    print('1', a)
    print('2', text_from_bits(a))

    test_message_array = encode_string(test_message)
    print(test_message_array)
    print(decode_string(test_message_array))
