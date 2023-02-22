import cv2
import numpy as np


def load_image(path):
    stream = open(path, 'rb')
    bytes = bytearray(stream.read())
    array = np.asarray(bytes, dtype=np.uint8)
    return cv2.imdecode(array, cv2.IMREAD_UNCHANGED)


def save_image(image, path):
    im = cv2.imencode(path[path.rfind('.'):], image)
    im = bytearray(im[1])
    stream = open(path, 'wb')
    stream.write(im)


def show_im(im, text="1"):
    cv2.imshow(text, im)


def set_waitkey(wk: int = 0):
    cv2.waitKey(wk)


def test():
    image = load_image("../data/images/Lena.jpg")
    show_im(image)

    save_image(image, "images/Lena_c.jpg")
    image = load_image("images/Lena_c.jpg")

    show_im(image)
    set_waitkey(0)


if __name__ == "__main__":
    test()
