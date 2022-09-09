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
helper function to find the difference
'''
def find_diff(b1, b2):
    diff = ""
    for i in range(len(b1)):
        if b1[i] != b2[i]:
            diff += b2[i]
            # print(diff)
    return diff

def find_diff_bit(b1, b2):
    for i in range(len(b1)):
        if (b1[i]!=b2[i]):
            if i < 5:
                print(b1, b2)
            return (8-i)
    return -1

"""
img1: unmodified image
img2: encoded image
"""
def show_data(img1, img2):
    lsb = 0
    diff = ""
    for row in range(len(img1)):
        orig_row = img1[row]  # original row
        enc_row = img2[row] # encoded row

        for col in range(len(img1[0])):
            orig_px = msg_to_bin(orig_row[col])
            enc_px = msg_to_bin(enc_row[col])

            for i in range(len(orig_px)):
                orig_bits = orig_px[i]
                enc_bits = enc_px[i]
                # if i==len(orig_px) - 1:
                #     print(orig_bits, enc_bits)
                if (orig_bits!=enc_bits):
                    x = find_diff_bit(orig_bits, enc_bits)# index at which the bytes start looking different
                    if (x > lsb) and (x - lsb < 3):
                        lsb = x
    #print(lsb)
    diff = ""
    for row in range(len(img1)):
        orig_row = img1[row]  # original row
        enc_row = img2[row] # encoded row
        for col in range(len(img1[0])):
            orig_px = msg_to_bin(orig_row[col])
            enc_px = msg_to_bin(enc_row[col])

            for i in range(len(orig_px)):
                orig_bits = orig_px[i]
                enc_bits = enc_px[i]
                if (orig_bits != enc_bits):
                    diff += enc_bits[-lsb:]


    allBytes = [diff[i: i + 8] for i in range(0, len(diff), 8)]  
    # Loop that goes through every single pixel for both image
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