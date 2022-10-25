import numpy as np
from scipy.fftpack import dct, idct


def PSNR(matrix1, matrix2):
    pixel_count = np.prod(matrix1.shape)
    s = np.sum(np.square(matrix1-matrix2))
    return 10*np.log2(pixel_count*(255**2)/s)


def compare_vectors(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)[:len(v1)]
    print(v1)
    print(v2)
    print(np.where(v1!=v2))
    print(len(v1[v1 == v2])/len(v1))
    return np.all(v1 == v2)


def calc_count_blocks(matrix: np.ndarray, block_size: int):
    matrix_size = matrix.shape
    col_count = int(np.floor(matrix_size[1] / block_size))
    row_count = int(np.floor(matrix_size[0] / block_size))
    blocks_count = col_count * row_count
    return blocks_count


def cut_into_blocks(matrix: np.ndarray, block_size: int):
    matrix_size = matrix.shape
    col_count = int(np.floor(matrix_size[1] / block_size))
    row_count = int(np.floor(matrix_size[0] / block_size))
    blocks_count = col_count * row_count

    cutted_matrix = np.zeros((blocks_count, block_size, block_size), dtype=int)

    for j in range(row_count):
        for i in range(col_count):
            cutted_matrix[i + j * col_count, :, :] \
                = matrix[j * block_size:(j + 1) * block_size, i * block_size:(i + 1) * block_size]

    return cutted_matrix


def normalize(matrix):
    min_v = np.min(matrix)
    matrix[matrix < 0] = 0

    max_v = np.max(matrix)
    if max_v > 255:
        matrix = (matrix / max_v) * 255
    return matrix


def unite_matris_blocks(matrix, size):
    block_size = matrix.shape[1]
    row_count = int(np.floor(size[0] / block_size))
    col_count = int(np.floor(size[1] / block_size))

    united_matrix = np.zeros((block_size*row_count, block_size*col_count))

    for j in range(row_count):
        for i in range(col_count):
            united_matrix[j * block_size:(j + 1) * block_size, i * block_size:(i + 1) * block_size] \
                = matrix[i + j * col_count, :, :]

    return united_matrix


def dct_blocks(array):
    dct_matrix = np.zeros(array.shape)
    i = 0
    for block in array:
        dct_matrix[i, :, :] = dct(dct(block.T, axis=0, norm="ortho").T, axis=0, norm="ortho")
        i += 1

    return dct_matrix


def idct_blocks(array):
    dct_matrix = np.zeros(array.shape)
    i = 0
    for block in array:
        dct_matrix[i, :, :] = idct(idct(block.T, axis=0, norm="ortho").T, axis=0, norm="ortho")
        i += 1

    return dct_matrix


def sum_mod(iterable):
    res = 0
    for i in iterable:
        res += np.abs(i)

    return res


def zig_val_iter(block_array, count_of_elements: int = None, start_row: int = 6, finish_row: int = 8):
    for cord in zig_index_iter(block_array.shape[0], count_of_elements, start_row, finish_row):
        yield block_array[cord]


def zig_index_iter(array_size, count_of_elements: int = None, start_row: int = 6, finish_row: int = 8):
    rows_count = array_size*2 - 1

    if not count_of_elements:
        count_of_elements = array_size**2

    if start_row < 0 or finish_row < 0:
        raise ValueError("row number must be higher or equals zero")
    elif finish_row < start_row:
        raise ValueError("start_row must be less or equals finish_row")
    elif finish_row >= rows_count or start_row >= rows_count:
        raise ValueError("row number value can't be higher than rows count")

    el_num = 0

    if start_row < array_size:
        for zig_row in range(start_row, array_size):

            if zig_row == finish_row+1:
                return

            row = zig_row
            for col in range(zig_row + 1):
                yield row, col

                el_num += 1
                if el_num == count_of_elements:
                    return

                row -= 1

        start_row = 1
    else:
        start_row -= array_size-1

    finish_row -= array_size-1
    for zig_col in range(start_row, array_size):

        if zig_col == finish_row+1:
            return

        row = array_size-1
        for col in range(zig_col, array_size):
            yield row, col

            el_num += 1
            if el_num == count_of_elements:
                return

            row -= 1