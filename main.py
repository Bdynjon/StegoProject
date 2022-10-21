import numpy as np

from image_funcs import load_image, show_im, set_waitkey, save_image
from stego import stego_code, stego_decode
from converters import encode_string, decode_string
from matrix_operations import compare_vectors, dct_blocks, cut_into_blocks


if __name__ == "__main__":
    container = load_image("images/sadov3.jpg")
    # container = np.ones((512, 512, 3))*100
    message = encode_string("Test message 1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")

    P = 50

    HF = (9, 15)
    LF = (1, 6)

    Pl = 2600
    Ph = 40

    rows = (7, 8)
    key = 1

    stego = stego_code(container, message, P, rows, key)
    # show_im(stego)

    save_image(stego, "images/stego.jpg")
    stego = load_image("images/stego.jpg")

    extr_message = stego_decode(stego, rows, key)
    extr_message = extr_message[:len(message)]

    print(compare_vectors(message, extr_message))

    print(decode_string(extr_message))

    show_im(container, "cont")
    show_im(stego, "stego")
    set_waitkey()





