
import string


def encrypt():
    with open('img.bmp', 'rb') as bmp_file:
        bmp = bmp_file.read()
    with open('text.txt', 'rb') as to_hide_file:
        to_hide = to_hide_file.read()

    hide_data(bmp, to_hide)


def decrypt():
    with open('img_hidden.bmp', 'rb') as bmp_file:
        bmp = bmp_file.read()

    start_offset = bmp[10]  # The byte at position 10 tells us where the color data starts

    # Deconstruct each byte and get its final bit
    bits = []
    for i in range(start_offset, len(bmp)):
        bits.append(nth_bit_present(bmp[i], 0))

    # Combine our bit array into bytes
    out_bytes = []
    for i in range(0, len(bits), 8):  # Take each 8-bit chunk
        if (len(bits) - i > 8):
            out_bytes.append(bits_to_byte(bits[i:i + 8]))

    # Convert bytes to characters
    out = []
    for b in out_bytes:
        out.append(chr(b))

    print(''.join(out))


def hide_data(bmp, data):
    start_offset = bmp[10]  # The byte at position 10 tells us where the color data starts

    bmpa = bytearray(bmp)
    data_array = data_to_bits(data)

    # We need to make sure there is enough space to hide our data
    assert len(data_array) < len(bmpa) + start_offset

    for i in range(len(data_array)):
        bmpa[i + start_offset] = set_final_bit(bmpa[i + start_offset], data_array[i])

    write_hidden_bmp(bmpa)


def data_to_bits(data):
    bits = []
    for i in range(len(data)):
        # A byte can at max be 8 digits long, i.e. 0b11111111 = 255
        # We start at the left most bit (position 7) and work down to 0
        for j in range(7, -1, -1):
            # Create the logic array of bits for our data
            bits.append(nth_bit_present(data[i], j))

    return bits


def set_final_bit(my_byte, ends_in_one):
    new_byte = 0
    if ends_in_one:
        if (nth_bit_present(my_byte, 0)):
            new_byte = my_byte  # No modification needed, it already ends in one
        else:
            new_byte = my_byte + 1
    else:
        if (nth_bit_present(my_byte, 0)):
            new_byte = my_byte - 1
        else:
            new_byte = my_byte  # No modification needed, it already ends in zero
    return new_byte


def nth_bit_present(my_byte, n):
    # Bitwise check to see what the nth bit is
    # If we get anything other than 0, it is TRUE else FALSE
    return (my_byte & (1 << n)) != 0


def bits_to_byte(bits):
    assert len(bits) == 8
    new_byte = 0
    for i in range(8):
        if bits[i] == True:
            # This bit==1 and the "position" we are at in the byte is 7-i
            # Bitwise OR will insert a 1 a this position
            new_byte |= 1 << 7 - i
        else:
            # This bit==0 and the "position" we are at in the byte is 7-i
            # Bitwise OR will insert a 0 a this position
            new_byte |= 0 << 7 - i
    return new_byte


def write_hidden_bmp(bytes_to_write):
    with open('img.bmp'.replace('.bmp', '_hidden.bmp'), 'wb') as out:
        out.write(bytes_to_write)

decrypt()

