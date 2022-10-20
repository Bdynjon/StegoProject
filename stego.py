import numpy as np
from matrix_operations import zig_val_iter, sum_mod, zig_index_iter, cut_into_blocks, dct_blocks, idct_blocks, \
    unite_matris_blocks, normalize
import copy


def insert(blocks, message, coefs_ind, P: int = 50):

    for i in range(len(message)):

        block = blocks[i]
        coef = coefs_ind[i]

        sec = block[coef[1][0], coef[1][1]]
        first = block[coef[0][0], coef[0][1]]

        sec_abs = abs(sec)
        first_abs = abs(first)

        sec_sign = -1 if sec < 0 else 1
        first_sign = -1 if first < 0 else 1

        if message[i] == 0:
            if first_abs - sec_abs <= P:
                ch = True
            block[coef[0][0], coef[0][1]] = (sec_abs + P + 1) * first_sign

        elif message[i] == 1:
            if first_abs - sec_abs >= -P:
                ch = True
            block[coef[1][0], coef[1][1]] = (first_abs + P + 1) * sec_sign

        blocks[i] = block


def extract(blocks, coefs_ind):
    message = []

    for i, block in enumerate(blocks):
        coef = coefs_ind[i]

        sec = block[coef[1][0], coef[1][1]]
        first = block[coef[0][0], coef[0][1]]

        if abs(first) > abs(sec):
            message.append(0)
        elif abs(first) < abs(sec):
            message.append(1)

    return message


def analyze_blocks(blocks, HF, LF, Ph, Pl):
    appropriate_blocks = []

    for i, block in enumerate(blocks):

        if analyze_block(block, HF, LF, Ph, Pl):
            appropriate_blocks.append(i)

    return appropriate_blocks


def analyze_block(block, HF, LF, Ph, Pl):
    SL = sum_mod(zig_val_iter(block, start_row=LF[0], finish_row=LF[1]))
    SH = sum_mod(zig_val_iter(block, start_row=HF[0], finish_row=HF[1]))

    if SL < Pl and SH > Ph:
        return True
    return False


def stego_code(container, message, P, rows, key=1):
    container_size = container.shape[:2]
    block_size = 8
    stego = copy.deepcopy(container)

    cutted_container = cut_into_blocks(stego[:, :, 0], block_size)
    count_blocks = cutted_container.shape[0]
    dct_block = dct_blocks(cutted_container)

    if count_blocks < len(message):
        raise ValueError("Choose shorter message or increase count of blocks")

    indexes = generate_indexes(rows, key, count_blocks)

    insert(dct_block, message, indexes, P)
    idct_block = idct_blocks(dct_block)
    normalize_blocks(idct_block)

    blue = unite_matris_blocks(idct_block, container_size)
    blue_size = blue.shape

    stego[:blue_size[0], :blue_size[1], 0] = blue[:, :]
    return stego


def stego_decode(stego, rows, key=1):
    block_size = 8

    cutted_container = cut_into_blocks(stego[:, :, 0], block_size)
    count_blocks = cutted_container.shape[0]
    dct_block = dct_blocks(cutted_container)

    indexes = generate_indexes(rows, key, count_blocks)

    return extract(dct_block, indexes)


def normalize_blocks(blocks):
    for i in range(len(blocks)):
        blocks[i] = np.round(normalize(blocks[i]))


def generate_indexes(rows, seed: int = -1, block_count: int = 1):
    generator = np.random.default_rng()
    if seed == -1:
        seed = generator.integers(0, 100000)
        generator = np.random.default_rng(seed)
    else:
        generator = np.random.default_rng(seed)

    index_vec = []
    for ind in zig_index_iter(8, start_row=rows[0], finish_row=rows[1]):
        index_vec.append(ind)

    index_vec = np.array(index_vec)
    ran = range(len(index_vec))
    res = []

    for i in range(block_count):
        ran = generator.permuted(ran)
        res.append(index_vec[ran[:2]])

    return res


def analyze_blocks(blocks, HF, LF, Ph, Pl):
    appropriate_blocks = []

    for i, block in enumerate(blocks):

        if analyze_block(block, HF, LF, Ph, Pl):
            appropriate_blocks.append(i)

    return appropriate_blocks


def analyze_block(block, HF, LF, Ph, Pl):
    SL = sum_mod(zig_val_iter(block, start_row=LF[0], finish_row=LF[1]))
    SH = sum_mod(zig_val_iter(block, start_row=HF[0], finish_row=HF[1]))

    if SL < Pl and SH > Ph:
        return True
    return False