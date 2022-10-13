import numpy as np

from loaders import load_image, show_im
from stego import stego_code, stego_decode
from converters import encode_string, decode_string
from matrix_operations import compare_vectors, dct_blocks, cut_into_blocks


if __name__ == "__main__":
    container = load_image("images/sadov3.jpg")
    # container = np.ones((512, 512, 3))*100
    message = encode_string("Test message")

    P = 10

    rows = (7, 8)
    key = 1

    stego = stego_code(container, message, P, rows, key)
    # show_im(stego)
    extr_message = stego_decode(stego, rows, key)
    extr_message = extr_message[:len(message)]
    show_im(stego)

    block_cont = cut_into_blocks(container[:, :, 0], 8)
    dct_cont = dct_blocks(block_cont)
    block_steg = cut_into_blocks(stego[:, :, 0], 8)
    dct_stego = dct_blocks(block_steg)
    diff = dct_cont - dct_stego

    print(compare_vectors(message, extr_message))

    print(decode_string(extr_message))






