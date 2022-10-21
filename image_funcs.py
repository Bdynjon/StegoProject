import cv2


def load_image(path):
    return cv2.imread(path)


def save_image(image, path):
    cv2.imwrite(path, image)


def show_im(im, text="1"):
    cv2.imshow(text, im)


def set_waitkey(wk: int = 0):
    cv2.waitKey(wk)