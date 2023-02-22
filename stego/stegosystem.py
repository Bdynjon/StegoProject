from tools import haming
from tools.matrix_operations import calc_count_blocks, fill_to_div
from tools.params import Params
from tools.key_loader import Key
from tools.converters import decode_image, encode_image, decode_string, encode_string
from stego.stego_coders import CoxJao
from tools.image_funcs import save_image, load_image
import cv2
import numpy as np


class StegoSystem:

    __slots__ = {
        '__first_im',
        '__second_im',
        '__im_message_insert',
        '__im_message_extract',
        '__key',
        '__param',
        '__stego_coder',
    }

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

    def set_key(self, seed: int):
        self.__key.seed = seed

    def set_params(self, P: int, rows: tuple, block_size: int, channels: dict):
        self.__param.set_params(P=P, rows=rows, block_size=block_size, channels=channels)

    def save_preset(self, path: str):
        self.__param.save_preset(path)

    def load_preset(self, path: str):
        self.__param.load_preset(path)
        return self.__param.P, self.__param.rows, self.__param.block_size, self.__param.channels

    def load_first_im(self, path):
        self.__first_im = load_image(path)
        self.__second_im = None

    def get_count_bits(self):
        if isinstance(self.__first_im, np.ndarray):
            block_size = self.__param.hamming_block_size if self.__param.hamming_block_size >= 4 else 0
            r = haming.calc_redundant_bits(block_size)
            blocks_count = calc_count_blocks(self.__first_im, self.__param.block_size)

            cg_c = 0
            for key in self.__param.channels:
                if self.__param.channels[key]:
                    cg_c += 1

            return (blocks_count//(1+r/block_size))*cg_c
        else:
            return 0

    def load_second_im(self, path):
        self.__second_im = load_image(path)

    def load_im_message_insert(self, path):
        self.__im_message_insert = load_image(path)
        self.__im_message_extract = None

    def get_inserted_image_len(self):
        return 24 + self.__im_message_insert.shape[0] * self.__im_message_insert.shape[1]

    def load_im_message_extract(self, path):
        self.__im_message_extract = load_image(path)

    def get_first_im(self):
        return self.__first_im

    def get_second_im(self):
        return self.__second_im

    def get_im_message_insert(self):
        if len(self.__im_message_insert.shape) != 3:
            return cv2.cvtColor(self.__im_message_insert, cv2.COLOR_GRAY2BGR)
        return self.__im_message_insert

    def get_im_message_extract(self):
        return self.__im_message_extract

    def save_second_im(self, path):
        save_image(self.__second_im, path)

    def save_extracted_image(self, path):
        save_image(self.__im_message_extract, path)
        self.__im_message_extract = None

    def decode(self, message_type: str = "string"):
        if not isinstance(self.__first_im, np.ndarray):
            raise AttributeError("Container hasn't loaded yet")

        message = self.__stego_coder.stego_decode(self.__first_im, self.__param, self.__key.seed)
        message = haming.from_hamming_code(message, self.__param.hamming_block_size)

        try:
            message = self.__convert_to_message(message, message_type)
        except:
            raise ValueError("Can't convert recived message to image")

        if message_type == "string":
            return message
        elif message_type == "image":
            self.__im_message_extract = message

    def encode(self, message=None, message_pype: str = "string"):
        if not isinstance(self.__first_im, np.ndarray):
            raise AttributeError("Container hasn't loaded yet")

        if message_pype == "string":
            message = self.__convert_to_bits(message)
        elif message_pype == "image":
            message = self.__convert_to_bits(self.__im_message_insert)

        message = haming.to_hamming_code(message, self.__param.hamming_block_size)

        self.__second_im = self.__stego_coder.stego_code(self.__first_im, message, self.__key.seed, self.__param)

    def __convert_to_bits(self, message):
        if isinstance(message, str):
            return fill_to_div(encode_string(message), self.__param.hamming_block_size)
        elif isinstance(message, np.ndarray):
            message = cv2.cvtColor(message, cv2.COLOR_BGR2GRAY)
            return fill_to_div(encode_image(message), self.__param.hamming_block_size)

    @staticmethod
    def __convert_to_message(bits, message_type: str = "string"):
        if message_type == "string":
            return decode_string(bits)
        elif message_type == "image":
            message = decode_image(bits)
            message = cv2.cvtColor(message, cv2.COLOR_GRAY2BGR)
            return message




