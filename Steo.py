from typing import Iterable
import numpy as np
from PIL import Image


def bits_provider(message) -> Iterable[int]:
    for char in message:
        ascii_value = ord(char)
        for bit_position in range(8):
            power = 7 - bit_position
            yield 1 if ascii_value & (1 << power) else 0


def chars_provider(pixel_red_values) -> Iterable[str]:
    ascii_value = 0
    for i, pixel_red_value in enumerate(pixel_red_values):
        ascii_value_bit_position = 7 - i % 8
        if pixel_red_value & 1:
            ascii_value |= 1 << ascii_value_bit_position
        if ascii_value_bit_position == 0:
            char: str = chr(ascii_value)
            if not char.isprintable() and char != '\n':
                return

            yield char

            ascii_value = 0


def create_image(message: str, input_filename, output_filename: str) -> None:
    img = Image.open(input_filename)
    pixels = np.array(img)
    img.close()
    clear_low_order_bits(pixels)
    for i, bit in enumerate(bits_provider(message)):
        row = i // pixels.shape[1]
        col = i % pixels.shape[1]
        pixels[row, col, 0] |= bit
    out_img = Image.fromarray(pixels)
    out_img.save(output_filename)
    out_img.close()


def clear_low_order_bits(pixels) -> None:
    for row in range(pixels.shape[0]):
        for col in range(pixels.shape[1]):
            pixels[row, col, 0] &= ~1


def encode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')

    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image
def decode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'


        # Main Function
def main():
    a = int(input(":: Welcome to Steganography ::\n"
                        "1. Encode\n2. Decode\n"))
    if (a == 1):
        encode()

    elif (a == 2):
        print("Decoded Word :  " + decode())
    else:
        raise Exception("Enter correct input")

# Driver Code
if __name__ == '__main__' :

    # Calling main function
    main()

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

