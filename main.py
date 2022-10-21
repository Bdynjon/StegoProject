import numpy as np
from params import Params
from image_funcs import load_image, show_im, set_waitkey, save_image
from stego import stego_code, stego_decode
from converters import encode_string, decode_string
from matrix_operations import compare_vectors, dct_blocks, cut_into_blocks


if __name__ == "__main__":
    #container = load_image("images/sadov3.jpg")[600:1000, 400:700]
    container = load_image("images/sadov3.jpg")
    # container = np.ones((512, 512, 3))*100
    message = encode_string("Test message")

    key = 1

    #настройка параметров встраивания
    params = Params()
    params.load_preset("params presets/my presets/test.json")

    #глубина встраивания
    params.P = 500

    #номера диагоналей(побочных) для встраивания(номерация с левого верхнего края)
    params.rows = (5, 6)

    #минимальная сумма высокочастотных коэффициентов
    params.Ph = 10
    params.save_preset("params presets/my presets/test.json")

    stego, approp_blocks = stego_code(container, message, key)
    # show_im(stego)

    save_image(stego, "images/stego.jpg")
    stego = load_image("images/stego.jpg")

    extr_message = stego_decode(stego, approp_blocks, key)
    extr_message = extr_message[:len(message)]

    print(compare_vectors(message, extr_message))

    print(decode_string(extr_message))

    show_im(container, "cont")
    show_im(stego, "stego")
    set_waitkey()





