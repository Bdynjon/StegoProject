import numpy as np
from params import Params
from image_funcs import load_image, show_im, set_waitkey, save_image
from stego import stego_code, stego_decode
from converters import encode_string, decode_string
from matrix_operations import compare_vectors, dct_blocks, cut_into_blocks, PSNR


if __name__ == "__main__":
    #container = load_image("images/sadov3.jpg")[600:1000, 400:700]
    container = load_image("images/sadov.png")
    # container = np.ones((512, 512, 3))*100
    message = encode_string("Test message11111111111111111111111111111111111111111111")

    key = 1

    #настройка параметров встраивания
    params = Params()
    params.load_preset()

    #глубина встраивания
    params.P = 40

    #номера диагоналей(побочных) для встраивания(номерация с левого верхнего угла)
    params.rows = (6, 7)

    #максимальная сумма высокочастотных коэффициентов
    params.Pl = 500000

    #минимальная сумма высокочастотных коэффициентов
    params.Ph = 10
    params.save_preset()

    stego = stego_code(container, message, key)
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





