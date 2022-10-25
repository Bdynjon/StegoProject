import numpy as np
from matrix_operations import zig_index_iter, cut_into_blocks, dct_blocks, idct_blocks, unite_matris_blocks, normalize
import copy


class CoxJao:
    def __insert(self, blocks, message, coefs_ind, approp_blocks, params):

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

    def __extract(self, blocks, coefs_ind, approp_block):
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

    def stego_code(self, container, message, seed, par):
        container_size = container.shape[:2]
        stego = copy.deepcopy(container)

        cutted_container, chen_count = self.__separate_channels(stego, par)

        dct_block = dct_blocks(cutted_container)

        count_blocks = len(dct_block)
        if count_blocks < len(message):
            raise ValueError("Choose shorter message or increase count of blocks")

        approp_blocks = self.__choose_blocks(count_blocks, seed, len(message))

        indexes = self.__generate_indexes(par.rows, seed, count_blocks)
        self.__insert(dct_block, message, indexes, approp_blocks, par)

        idct_block = idct_blocks(dct_block)
        self.__normalize_blocks(idct_block)

        return self.__unite_channels(stego, idct_block, count_blocks, chen_count, par, container_size)

    def __separate_channels(self, stego, par):
        cutted_container = None
        chen_count = 0

        if par.channels["blue"]:
            cutted_container = cut_into_blocks(stego[:, :, 0], par.block_size)
            chen_count += 1

        if par.channels["green"]:
            cutted_container = np.vstack((cutted_container, cut_into_blocks(stego[:, :, 1], par.block_size))) if \
                isinstance(cutted_container, np.ndarray) else cut_into_blocks(stego[:, :, 1], par.block_size)
            chen_count += 1

        if par.channels["red"]:
            cutted_container = np.vstack((cutted_container, cut_into_blocks(stego[:, :, 2], par.block_size))) if \
                isinstance(cutted_container, np.ndarray) else cut_into_blocks(stego[:, :, 2], par.block_size)

        return cutted_container, chen_count

    def __unite_channels(self, stego, idct_block, count_blocks, chen_count, par, container_size):
        interv = [[int(i * count_blocks / chen_count), int((i + 1) * count_blocks / chen_count)] for i in
                  range(chen_count)]
        i = 0
        print(interv)

        if par.channels["blue"]:
            united = unite_matris_blocks(idct_block[interv[i][0]:interv[i][1], :, :], container_size)
            size = united.shape
            stego[:size[0], :size[1], 0] = united[:, :]
            i += 1

        if par.channels["green"]:
            united = unite_matris_blocks(idct_block[interv[i][0]:interv[i][1], :, :], container_size)
            size = united.shape
            stego[:size[0], :size[1], 1] = united[:, :]
            i += 1

        if par.channels["red"]:
            united = unite_matris_blocks(idct_block[interv[i][0]:interv[i][1], :, :], container_size)
            size = united.shape
            stego[:size[0], :size[1], 2] = united[:, :]

        return stego

    def stego_decode(self, stego, par, key):
        cutted_container = cut_into_blocks(stego[:, :, 0], par.block_size)
        dct_block = dct_blocks(cutted_container)
        block_count = len(dct_block)

        indexes = self.__generate_indexes(par.rows, key, block_count)
        approp_blocks = self.__choose_blocks(block_count, key, block_count)

        return self.__extract(dct_block, indexes, approp_blocks)

    def __normalize_blocks(self, blocks):
        for i in range(len(blocks)):
            blocks[i] = np.round(normalize(blocks[i]))

    def __choose_blocks(self, block_count, seed, length):
        generator = np.random.default_rng(seed)
        ran = range(block_count)
        ran = generator.permuted(ran)

        return ran[:length]

    def __generate_indexes(self, rows, seed: int = 1, block_count: int = 1):
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