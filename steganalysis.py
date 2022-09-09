import numpy as np
import cv2

NUM_LSB = 8

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

"""
img1: unmodified image
img2: encoded image
"""
def show_data(img1, img2):

    # Loop that goes through every single pixel for both image
    for bytes in allBytes:  
        decodedData += chr(int(bytes, 2))  
        # checking if we have reached the delimiter which is "#####"  
        if decodedData[-5:] == "#####":  
            break