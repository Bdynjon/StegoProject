import numpy as np
from matrix_operations import zig_val_iter, sum_mod, zig_index_iter, cut_into_blocks, dct_blocks, idct_blocks, \
    unite_matris_blocks, normalize
import copy
from params import Params


def insert(blocks, message, coefs_ind, approp_blocks, params):

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
            if diff < -0.7*params.P:
                inserted = False
            elif diff <= params.P:
                    block[coef[0][0], coef[0][1]] = (sec_abs + params.P) * first_sign
                    #block[coef[1][0], coef[1][1]] = (sec_abs - params.P / 2 - 1) * sec_sign

        elif message[m] == 1:
            if diff > 0.7*params.P:
                inserted = False
            elif diff >= -params.P:
                block[coef[1][0], coef[1][1]] = (first_abs + params.P) * sec_sign
                #block[coef[0][0], coef[0][1]] = (first_abs - params.P / 2 - 1) * first_sign

        if m == 197:
            print(m)
            print(message[m])
            print(block)
            print(first, sec)
            print(block[coef[0][0], coef[0][1]], block[coef[1][0], coef[1][1]])
            print("____________")

        if inserted:
            blocks[block_ind] = block
            m+=1
        else:
            print(block_ind, "---")
            del(approp_blocks[approp_blocks.index(block_ind)])

        return approp_blocks


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

        if m == 197:
            print(m)
            print(message[m])
            print(block)
            print(first)
            print(sec)
            print("____________")

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


def stego_code(container, message, key):
    container_size = container.shape[:2]
    stego = copy.deepcopy(container)

    par = Params()

    cutted_container = cut_into_blocks(stego[:, :, 0], par.block_size)
    dct_block = dct_blocks(cutted_container)

    approp_blocks = analyze_blocks(dct_block, par.HF, par.LF, par.Ph, par.Pl)
    count_blocks = len(approp_blocks)

    if count_blocks < len(message):
        raise ValueError("Choose shorter message or increase count of blocks")

    indexes = generate_indexes(par.rows, key, count_blocks)
    approp_blocks = insert(dct_block, message, indexes, approp_blocks, par)
    idct_block = idct_blocks(dct_block)
    normalize_blocks(idct_block)

    blue = unite_matris_blocks(idct_block, container_size)
    blue_size = blue.shape

    stego[:blue_size[0], :blue_size[1], 0] = blue[:, :]
    return stego, approp_blocks


def stego_decode(stego, approp_block, key):
    par = Params()

    cutted_container = cut_into_blocks(stego[:, :, 0], par.block_size)
    count_blocks = len(approp_block)
    dct_block = dct_blocks(cutted_container)

    indexes = generate_indexes(par.rows, key, count_blocks)

    return extract(dct_block, indexes, approp_block)


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
