from loaders import load_image, show_im
from stego import stego_code, stego_decode
from converters import encode_string, decode_string
from matrix_operations import compare_vectors, dct_blocks, cut_into_blocks


if __name__ == "__main__":
    container = load_image("images/sadov3.jpg")[450:900, 340:650, :]
    message = encode_string("S")

    HF = (9, 14)
    LF = (1, 6)

    #Pl = 2600
    #Ph = 40

    Pl = 2000
    Ph = 40

    P = 5

    rows = (7, 8)

    stego = stego_code(container, message, P, HF, LF, Ph, Pl, rows)
    # show_im(stego)
    extr_message = stego_decode(stego, P, HF, LF, Ph, Pl, rows)
    extr_message = extr_message[:len(message)]
    show_im(stego)

    block_cont = cut_into_blocks(container[:, :, 0], 8)
    dct_cont = dct_blocks(block_cont)
    block_steg = cut_into_blocks(stego[:, :, 0], 8)
    dct_stego = dct_blocks(block_steg)
    diff = dct_cont - dct_stego
    print(block_steg[286])
    print(block_cont[286])

    print(compare_vectors(message, extr_message))

    print(decode_string(extr_message))






