import numpy as np
from matrix_operations import zig_val_iter, sum_mod, zig_index_iter, cut_into_blocks, dct_blocks, idct_blocks, \
    unite_matris_blocks, normalize
import copy
from params import Params
from key_loader import Key


def insert_t(blocks, message, coefs_ind, approp_blocks, params):

    m = 0
    for block_ind in approp_blocks:
        if m >= len(message):
            break

        block = blocks[block_ind]
        coef = coefs_ind[m]

        sec = block[coef[1][0], coef[1][1]]
        first = block[coef[0][0], coef[0][1]]

        sec_abs = abs(sec)
        first_abs = abs(first)

        sec_sign = -1 if sec < 0 else 1
        first_sign = -1 if first < 0 else 1

        diff = first_abs - sec_abs
        inserted = True

        if message[m] == 0:
            if diff <= params.P:
                if diff > (-0.5 * params.P):
                    block[coef[0][0], coef[0][1]] = (sec_abs + params.P) * first_sign
                    # block[coef[1][0], coef[1][1]] = (sec_abs - params.P / 2 - 1) * sec_sign
                else:
                    inserted = False

        elif message[m] == 1:
            if diff >= -params.P:
                if diff < 0.5 * params.P:
                    block[coef[1][0], coef[1][1]] = (first_abs + params.P) * sec_sign
                    # block[coef[0][0], coef[0][1]] = (first_abs - params.P / 2 - 1) * first_sign
                else:
                    inserted = False

        if inserted:
            blocks[block_ind] = block
            m += 1
        else:
            print(block_ind)
            del(approp_blocks[approp_blocks.index(block_ind)])

    return approp_blocks


def insert(blocks, message, coefs_ind, approp_blocks, params):

    for m, block_ind in enumerate(approp_blocks):
        if m >= len(message):
            break

        block = blocks[block_ind]
        coef = coefs_ind[m]

        sec = block[coef[1][0], coef[1][1]]
        first = block[coef[0][0], coef[0][1]]

        sec_abs = abs(sec)
        first_abs = abs(first)

        sec_sign = -1 if sec < 0 else 1
        first_sign = -1 if first < 0 else 1

        diff = first_abs - sec_abs

        if message[m] == 0:
            if diff <= params.P:
                block[coef[0][0], coef[0][1]] = (sec_abs + params.P) * first_sign
                # block[coef[1][0], coef[1][1]] = (sec_abs - params.P / 2 - 1) * sec_sign

        elif message[m] == 1:
            if diff >= -params.P:
                block[coef[1][0], coef[1][1]] = (first_abs + params.P) * sec_sign
                # block[coef[0][0], coef[0][1]] = (first_abs - params.P / 2 - 1) * first_sign

        blocks[block_ind] = block


def extract(blocks, coefs_ind, approp_block):
    message = []

    for m, block_ind in enumerate(approp_block):
        block = blocks[block_ind]
        coef = coefs_ind[m]

        sec = block[coef[1][0], coef[1][1]]
        first = block[coef[0][0], coef[0][1]]

        if abs(first) > abs(sec):
            message.append(0)
        elif abs(first) < abs(sec):
            message.append(1)

    return message


def stego_code(container, message, seed):
    container_size = container.shape[:2]
    stego = copy.deepcopy(container)

    par = Params()

    cutted_container = cut_into_blocks(stego[:, :, 0], par.block_size)
    dct_block = dct_blocks(cutted_container)

    count_blocks = len(dct_block)
    if count_blocks < len(message):
        raise ValueError("Choose shorter message or increase count of blocks")

    approp_blocks = choose_blocks(count_blocks, seed, len(message))

    indexes = generate_indexes(par.rows, seed, count_blocks)
    insert(dct_block, message, indexes, approp_blocks, par)

    idct_block = idct_blocks(dct_block)
    normalize_blocks(idct_block)

    blue = unite_matris_blocks(idct_block, container_size)
    blue_size = blue.shape

    stego[:blue_size[0], :blue_size[1], 0] = blue[:, :]

    return stego


def stego_decode(stego):
    par = Params()
    key = Key()

    cutted_container = cut_into_blocks(stego[:, :, 0], par.block_size)
    dct_block = dct_blocks(cutted_container)
    block_count = len(dct_block)

    indexes = generate_indexes(par.rows, key.seed, block_count)
    approp_blocks = choose_blocks(block_count, key.seed, block_count)

    return extract(dct_block, indexes, approp_blocks)


def normalize_blocks(blocks):
    for i in range(len(blocks)):
        blocks[i] = np.round(normalize(blocks[i]))


def choose_blocks(block_count, seed, length):
    generator = np.random.default_rng(seed)
    ran = range(block_count)
    ran = generator.permuted(ran)

    return ran[:length]


def generate_indexes(rows, seed: int = 1, block_count: int = 1):
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
