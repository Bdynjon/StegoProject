import numpy as np
from params import Params
from image_funcs import load_image, show_im, set_waitkey
from stegosystem import StegoSystem
from converters import encode_string, decode_string
from matrix_operations import compare_vectors, dct_blocks, cut_into_blocks, PSNR


if __name__ == "__main__":

    ss = StegoSystem()
    message = "images/MilkyWay.jpg"
    ss.load_first_im(message)
    container = ss.get_first_im()
    key = 1

    message = "Test message11111111111111111111111111111111111111111111"

    #настройка параметров встраивания
    params = Params()

    params.channels['blue'] = True
    params.channels['green'] = False
    params.channels['red'] = False

    #глубина встраивания
    params.P = 70

    #номера диагоналей(побочных) для встраивания(номерация с левого верхнего угла)
    params.rows = (6, 7)

    params.hamming_block_size = 8
    params.save_preset()

    ss.code(key, message)
    ss.save_second_im("images/stego/stego.png")

    stego = ss.get_second_im()
    stego_1 = load_image("images/stego/stego.jpg")

    print(stego - stego_1)

    ss.load_first_im("images/stego/stego.jpg")
    extr_message = ss.decode(key)

    print(PSNR(container, stego_1))

    print(compare_vectors(encode_string(message), encode_string(extr_message)))

    print(extr_message)

    show_im(container, "cont")
    show_im(stego, "stego")
    set_waitkey()





