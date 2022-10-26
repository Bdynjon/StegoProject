import numpy as np
from matrix_operations import calc_count_blocks
from params import Params
from key_loader import Key
import cv2
from converters import decode_image, encode_image, decode_string, encode_string
from stego_coders import CoxJao
from haming import to_hamming_code, from_hamming_code

class StegoSystem:

    def __init__(self, stego_coder=CoxJao):
        self.__first_im = None
        self.__second_im = None

        self.__im_message_insert = None
        self.__im_message_extract = None

        self.__key = Key()
        self.__param = Params()

        self.__stego_coder = stego_coder()

    def load_key(self, path: str):
        self.__key.load_key(path)
        return self.__key.seed

    def save_key(self, seed: int, path: str):
        self.__key.seed = seed
        self.__key.save_key(path)

    def set_params(self, P: int, rows: tuple, block_size: int, channels: dict, hamming_block_size: int):
        self.__param.set_params(P, rows, block_size, channels, hamming_block_size)

    def save_preset(self, path: str):
        self.__param.save_preset(path)

    def load_preset(self, path: str):
        self.__param.load_preset(path)
        return self.__param.P, self.__param.rows, self.__param.block_size, self.__param.channels

    def load_first_im(self, path):
        self.__first_im = cv2.imread(path)
        return calc_count_blocks(self.__first_im, self.__param.block_size)

    def load_second_im(self, path):
        self.__second_im = cv2.imread(path)

    def load_im_message_insert(self, path):
        self.__im_message_insert = cv2.imread(path)

    def load_im_message_extract(self, path):
        self.__im_message_extract = cv2.imread(path)

    def get_first_im(self):
        return self.__first_im

    def get_second_im(self):
        return self.__second_im

    def get_im_message_insert(self):
        return self.__im_message_insert

    def get_im_message_extract(self):
        return self.__im_message_extract

    def save_second_im(self, path):
        cv2.imwrite(path, self.__second_im)

    def save_extracted_image(self, path):
        cv2.imwrite(path, self.__im_message_extract)

    def code(self, key, message=None, message_pype: str = "string"):
        if message_pype == "string":
            message = self.__convert_to_bits(message)
        elif message_pype == "image":
            message = self.__convert_to_bits(self.__im_message_insert)

        message = to_hamming_code(message, self.__param.hamming_block_size)

        if not isinstance(self.__first_im, np.ndarray):
            raise AttributeError("Container hasn't loaded yet")

        self.__second_im = self.__stego_coder.stego_code(self.__first_im, message, key, self.__param)

    def __convert_to_bits(self, message):
        if isinstance(message, str):
            return encode_string(message)
        elif isinstance(message, np.ndarray):
            return encode_image(message)

    def __convert_to_message(self, bits, message_type: str = "string"):
        if message_type == "string":
            return decode_string(bits)
        elif message_type == "image":
            return decode_image(bits)

    def decode(self, key: int, message_type: str = "string"):
        message = self.__stego_coder.stego_decode(self.__first_im, self.__param, key)
        message = from_hamming_code(message, self.__param.hamming_block_size)

        try:
            message = self.__convert_to_message(message, message_type)
        except:
            raise ValueError("Can't convert recived message to image")

        return message


