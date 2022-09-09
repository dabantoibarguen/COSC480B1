# COSC 480B HW 1 Part 2
# Group Members: Diego Abanto, Jin Sohn, Sara Alam

import numpy as np
import cv2

NUM_LSB = 3

# convert the message to binary
def msg_to_bin(msg):  
    if type(msg) == str:  
        return ''.join([format(ord(i), "08b") for i in msg])  
    elif type(msg) == bytes or type(msg) == np.ndarray:  
        return [format(i, "08b") for i in msg]  
    elif type(msg) == int or type(msg) == np.uint8:  
        return format(msg, "08b")  
    else:  
        raise TypeError("Input type not supported")

'''
helper function to find the first bit that is different
'''
def find_diff_bit(b1, b2):
    for i in range(len(b1)):
        # as soon as two bits differ, return (8 - index)
        if (b1[i]!=b2[i]):
            return (8-i)
    return -1

"""
img1: unmodified image
img2: encoded image
"""
def show_data(img1, img2):
    # 1. Infer how many LSBs were modified, at what "skip" or interval
    lsb_dict = {} # key = LSBs, value = frequency at which this many LSBs were modified
    skip_dict = {} # key = skipped pixels, values = frequency
    skipped = 0
    last_diff_row = -1
    last_diff_col = -1
    for row in range(len(img1)):
        orig_row = img1[row]  # original row
        enc_row = img2[row] # encoded row
        for col in range(len(img1[0])):
            orig_px = msg_to_bin(orig_row[col])
            enc_px = msg_to_bin(enc_row[col])
            for i in range(len(orig_px)):
                orig_bits = orig_px[i]
                enc_bits = enc_px[i]
                if (orig_bits!=enc_bits):
                    last_diff_row = row
                    last_diff_col = col
                    if skipped not in skip_dict:
                        skip_dict[skipped] = 0
                    skip_dict[skipped] += 1
                    skipped = 0
                    x = find_diff_bit(orig_bits, enc_bits)# index at which the bytes start looking different
                    if x not in lsb_dict:
                        lsb_dict[x] = 0
                    lsb_dict[x]+= 1
                else:
                    skipped += 1
    lsb = 0
    max_f = 0
    for l in lsb_dict:
        f = lsb_dict[l]
        if f > max_f:
            max_f = f
            lsb = l

    skipp = 1
    max_f2 = 0
    for skip in skip_dict:
        f = skip_dict[skip]
        if f > max_f2:
            max_f2 = f
            skipp = skip

    # 2. Accumulate LSBs of the pixels that differ from the original image, at the most likely skip
    diff = ""
    skip2 = 0
    for row in range(last_diff_row + 1):
        orig_row = img1[row]  # original row
        enc_row = img2[row] # encoded row
        for col in range(len(orig_row)):
            orig_px = msg_to_bin(orig_row[col])
            enc_px = msg_to_bin(enc_row[col])

            for i in range(len(orig_px)):
                orig_bits = orig_px[i]
                enc_bits = enc_px[i]
                if (orig_bits != enc_bits) or (skip2 == skipp):
                    if (row == last_diff_row) and (col >= last_diff_col) and (len(diff)%8 != 0):
                        break
                    skip2 = 0
                    diff += enc_bits[-lsb:]
                else:
                    skip2 += 1


    # 3. break the accumulated bits into bytes, then convert to characters
    allBytes = [diff[i: i + 8] for i in range(0, len(diff), 8)]  
    decodedData = ""
    for bytes in allBytes:  
        decodedData += chr(int(bytes, 2))

    return decodedData

def main():
    img1_name = input("Enter unmodified image name (with extension): ")  
    img1 = cv2.imread(img1_name)
    img2_name = input("Enter the name of the Steganographic image that has to be decoded (with extension): ")  
    img2 = cv2.imread(img2_name)  # reading the image using the imread() function  
    text = show_data(img1, img2)
    print(text)

main()