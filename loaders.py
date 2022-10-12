import cv2


def load_image(path):
    return cv2.imread(path)


def show_im(im):
    cv2.imshow("1", im)
    cv2.waitKey(0)