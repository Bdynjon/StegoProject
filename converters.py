import cv2
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


def encode_image(image):
    size = image.shape
    array = []
    size_arr = bin(size[0])[2:].zfill(12) + bin(size[1])[2:].zfill(12)
    image = image / 255

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
    print(size)

    image = np.zeros(size)

    for i in range(size[0]):
        for j in range(size[1]):
            image[i,j] = array[j + i*size[1] + 24] * 255

    return image


if __name__ == "__main__":
    test_im = np.zeros((300, 300))
    test_im[20:40, 20:40] = 255

    cv2.imshow("test_im", test_im)

    array = encode_image(test_im)
    rec_im = decode_image(array)

    cv2.imshow("rec_im", rec_im)

    print(np.all(test_im == rec_im))

    cv2.waitKey(0)
