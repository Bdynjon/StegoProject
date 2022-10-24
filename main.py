import numpy as np
from params import Params
from image_funcs import load_image, show_im, set_waitkey, save_image
from stego import stego_code, stego_decode
from converters import encode_string, decode_string
from matrix_operations import compare_vectors, dct_blocks, cut_into_blocks, PSNR
from key_loader import Key


if __name__ == "__main__":
    container = load_image("images/MilkyWay.jpg")
    message = encode_string("Test message11111111111111111111111111111111111111111111")

    key = Key()
    key.seed = 1
    key.save_key()

    #настройка параметров встраивания
    params = Params()
    params.load_preset()

    #глубина встраивания
    params.P = 100

    #номера диагоналей(побочных) для встраивания(номерация с левого верхнего угла)
    params.rows = (6, 7)
    params.save_preset()

    stego = stego_code(container, message, key.seed)
    # show_im(stego)

    save_image(stego, "images/stego/stego.jpg")
    stego = load_image("images/stego/stego.jpg")

    extr_message = stego_decode(stego)

    print(PSNR(container, stego))

    print(compare_vectors(message, extr_message))

    print(decode_string(extr_message))

    show_im(container, "cont")
    show_im(stego, "stego")
    set_waitkey()





