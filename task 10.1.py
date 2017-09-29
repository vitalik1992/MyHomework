import string


def encrypt():
    img = input('Введіть адрес зображення для шифрування : ')
    text = input('Введіть адрес текстового файлу який потрібно зашифрувати : ')
    with open(img, 'rb') as bmp_file:
        bmp = bmp_file.read()
    with open(text, 'rb') as to_hide_file:
        to_hide = to_hide_file.read()

    hide_data(bmp, to_hide)


def decrypt():
    with open('img_hidden.bmp', 'rb') as bmp_file:
        bmp = bmp_file.read()

    start_offset = bmp[10]


    bits = []
    for i in range(start_offset, len(bmp)):
        bits.append(nth_bit_present(bmp[i], 0))


    out_bytes = []
    for i in range(0, len(bits), 8):
        if (len(bits) - i > 8):
            out_bytes.append(bits_to_byte(bits[i:i + 8]))


    out = []
    for b in out_bytes:
        out.append(chr(b))

    print(''.join(out))


def hide_data(bmp, data):
    start_offset = bmp[10]
    bmpa = bytearray(bmp)
    data_array = data_to_bits(data)


    assert len(data_array) < len(bmpa) + start_offset

    for i in range(len(data_array)):
        bmpa[i + start_offset] = set_final_bit(bmpa[i + start_offset], data_array[i])

    write_hidden_bmp(bmpa)


def data_to_bits(data):
    bits = []
    for i in range(len(data)):

        for j in range(7, -1, -1):

            bits.append(nth_bit_present(data[i], j))

    return bits


def set_final_bit(my_byte, ends_in_one):
    new_byte = 0
    if ends_in_one:
        if (nth_bit_present(my_byte, 0)):
            new_byte = my_byte
        else:
            new_byte = my_byte + 1
    else:
        if (nth_bit_present(my_byte, 0)):
            new_byte = my_byte - 1
        else:
            new_byte = my_byte
    return new_byte


def nth_bit_present(my_byte, n):

    return (my_byte & (1 << n)) != 0


def bits_to_byte(bits):
    assert len(bits) == 8
    new_byte = 0
    for i in range(8):
        if bits[i] == True:

            new_byte |= 1 << 7 - i
        else:

            new_byte |= 0 << 7 - i
    return new_byte


def write_hidden_bmp(bytes_to_write):
    with open('img.bmp'.replace('.bmp', '_hidden.bmp'), 'wb') as out:
        out.write(bytes_to_write)

def main():
    ask = input(' Do you want to encrypt or decrypt  ? enc/dec : ')
    if ask == 'enc':
        encrypt()
    else:
        decrypt()


if __name__ == '__main__':
    main()

