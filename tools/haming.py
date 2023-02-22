import numpy as np


def calc_redundant_bits(m):
    for i in range(m):
        if 2 ** i >= m + i + 1:
            return i


def pos_redundant_bits(data, r):
    j = 0
    k = 1
    m = len(data)
    res = ''

    for i in range(1, m + r + 1):
        if i == 2 ** j:
            res = res + '0'
            j += 1
        else:
            res = res + str(data[-1 * k])
            k += 1

    return res[::-1]


def calc_parity_bits(arr, r):
    n = len(arr)

    for i in range(r):
        val = 0
        for j in range(1, n + 1):

            if j & (2 ** i) == (2 ** i):
                val = val ^ int(arr[-1 * j])

        arr = arr[:n - (2 ** i)] + str(val) + arr[n - (2 ** i) + 1:]
    return arr


def detect_error(arr, nr):
    n = len(arr)
    res = 0

    for i in range(nr):
        val = 0
        for j in range(1, n + 1):
            if (j & (2 ** i) == (2 ** i)):
                val = val ^ int(arr[-1 * j])

        res = res + val * (10 ** i)

    return int(str(res), 2)


def to_hamming_code(data, size_block):

    if size_block < 4:
        return data

    m = len(data)
    r = calc_redundant_bits(size_block)
    newdata = []

    for i in range(m // size_block):
        data_block = data[i * size_block:(i + 1) * size_block]
        arr = pos_redundant_bits(data_block, r)
        arr = calc_parity_bits(arr, r)
        newdata += [int(x) for x in arr]

    return newdata


def from_hamming_code(data, size_block):

    if size_block < 4:
        return data

    m = len(data)
    r = calc_redundant_bits(size_block)
    full_size_block = r + size_block
    newdata_from_hamming = []
    indexes = [2 ** x for x in range(r)]

    for i in range(m // full_size_block):
        data_block = data[i * full_size_block:(i + 1) * full_size_block]
        correction = detect_error(data_block, r)

        if correction != 0:
            data_block[len(data_block) - correction] = 1 - data_block[len(data_block) - correction]

        newdata = [data_block[-x] for x in range(1, len(data_block) + 1) if x not in indexes]
        newdata.reverse()
        newdata_from_hamming += newdata

    return newdata_from_hamming


def test():
    gen = np.random.default_rng(1)

    size_data = 15
    size_block = 8

    data = [i for i in gen.integers(low=0, high=2, size=size_data)]

    for i in range(len(data) // size_block):
        print(data[i * size_block:(i + 1) * size_block])

    print("-------")

    new_data = to_hamming_code(data, size_block)
    size_block_2 = size_block + calc_redundant_bits(size_block)
    print(new_data)

    # new_data[0] = 1
    # new_data[13] = 0
    # new_data[31] = 1

    new_data_2 = from_hamming_code(new_data, size_block)

    for i in range(len(new_data_2) // size_block):
        print(new_data_2[i * size_block:(i + 1) * size_block])


if __name__ == "__main__":
    test()
