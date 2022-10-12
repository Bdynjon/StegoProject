import numpy as np
from matrix_operations import zig_val_iter, sum_mod, zig_index_iter, cut_into_blocks, dct_blocks, idct_blocks, \
    unite_matris_blocks, normalize
import copy


def insert(blocks, message, blocks_ind, coefs_ind, P: int = 50):
    block_count = len(blocks_ind)

    for i in range(block_count):
        if i == len(message):
            break
        block = blocks[blocks_ind[i]]
        coef = coefs_ind[i]

        third = block[coef[2][0], coef[2][1]]
        sec = block[coef[1][0], coef[1][1]]
        first = block[coef[0][0], coef[0][1]]
        if i == 0:
            print(blocks_ind[i])
            print(block)
            print(coef)
            print(third, sec, first)

        ch = False

        if message[i] == 0:
            m = min(first, sec)
            if third >= m:
                ch = True
                block[coef[2][0], coef[2][1]] = m - int(P/2)
                if first == m:
                    block[coef[0][0], coef[0][1]] += int(P/2)
                else:
                    block[coef[1][0], coef[1][1]] += int(P/2)
        elif message[i] == 1:
            m = max(first, sec)
            if third <= m:
                block[coef[2][0], coef[2][1]] = m + int(P/2)
                ch = True
                if first == m:
                    block[coef[0][0], coef[0][1]] -= int(P/2)
                else:
                    block[coef[1][0], coef[1][1]] -= int(P/2)
        if i == 0:
            print(block)
            print(message[i])
            print(ch)

        blocks[blocks_ind[i]] = block


def extract(blocks, blocks_ind, coefs_ind, P):
    message = []

    for i, b_ind in enumerate(blocks_ind):
        block = blocks[b_ind]
        coef = coefs_ind[i]

        third = block[coef[2][0], coef[2][1]]
        sec = block[coef[1][0], coef[1][1]]
        first = block[coef[0][0], coef[0][1]]

        if i == 0:
            print(b_ind)
            print(block)
            print(coef)
            print(third, sec, first)

        if third < min(sec, first) - P:
            message.append(0)
        elif third > max(sec, first) + P:
            message.append(1)

    return message


def stego_code(container, message, P, HF, LF, Ph, Pl, rows):
    container_size = container.shape[:2]
    block_size = 8
    stego = copy.deepcopy(container)

    cutted_container = cut_into_blocks(stego[:, :, 0], block_size)
    count_blocks = cutted_container.shape[0]
    dct_block = dct_blocks(cutted_container)

    approp_blocks = analyze_blocks(dct_block, HF, LF, Ph, Pl)
    max_bits_count = len(approp_blocks)

    if max_bits_count < len(message):
        raise ValueError("Choose shorter message or increase count of blocks")

    indexes = generate_indexes(rows, 1, count_blocks)

    insert(dct_block, message, approp_blocks, indexes, P)
    idct_block = idct_blocks(dct_block)
    normalize_blocks(idct_block, approp_blocks)

    blue = unite_matris_blocks(idct_block, container_size)
    blue_size = blue.shape

    stego[:blue_size[0], :blue_size[1], 0] = blue[:, :]
    return stego


def stego_decode(stego, P, HF, LF, Ph, Pl, rows):
    block_size = 8

    cutted_container = cut_into_blocks(stego[:, :, 0], block_size)
    count_blocks = cutted_container.shape[0]
    dct_block = dct_blocks(cutted_container)

    approp_blocks = analyze_blocks(dct_block, HF, LF, Ph, Pl)
    indexes = generate_indexes(rows, 1, count_blocks)

    return extract(dct_block, approp_blocks, indexes, P)


def normalize_blocks(blocks, indexes):
    for j, i in enumerate(indexes):
        if j == 0:
            print("_______________")
            print(blocks[i])
        blocks[i] = np.round(normalize(blocks[i]))
        if j == 0:
            print(blocks[i])


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
        res.append(index_vec[ran[:3]])

    return res


def analyze_blocks(blocks, HF, LF, Ph, Pl):
    blocks_count = blocks.shape[0]
    appropriate_blocks = []

    for i in range(blocks_count):
        SL = sum_mod(zig_val_iter(blocks[i], start_row=LF[0], finish_row=LF[1]))
        SH = sum_mod(zig_val_iter(blocks[i], start_row=HF[0], finish_row=HF[1]))
        # print(SL)
        # print(SH)
        # print("_____________")

        if SL < Pl and SH > Ph:
            appropriate_blocks.append(i)

    return appropriate_blocks
