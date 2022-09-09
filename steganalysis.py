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

"""
img1: unmodified image
img2: encoded image
"""
def show_data(img1, img2):
    diff = ""
    # for row in range(len(img1)):
    #     orig_row = img1[row]  # original row
    #     enc_row = img2[row] # encoded row
    #     for col in range(len(img1[0])):
    #         # r,g,b = msg_to_bin(orig_row[col])
    #         # print(r,g,b)
    #         orig_px = msg_to_bin(orig_row[col])
    #         # print(type(orig_px[0]))
    #         enc_px = msg_to_bin(enc_row[col])
    #         # print(len(orig_px))
    #         # converting RGB values to binary format  
    #         for i in range(len(orig_px)):
    #             orig_bits = orig_px[i]
    #             enc_bits = enc_px[i]
    #             diff += find_diff(orig_bits, enc_bits) # because checking is already O(n)
    bin_data1 = ""  
    for values in img1:  
        for pixels in values:  
            # converting the Red, Green, Blue values into binary format  
            r, g, b = msg_to_bin(pixels)  
            bin_data1 += r
            bin_data1 += g
            bin_data1 += b
            # modifying the LSB only if there is data remaining to store  
    # print(diff)
    bin_data2 = ""  
    for values in img2:  
        for pixels in values:  
            # converting the Red, Green, Blue values into binary format  
            r, g, b = msg_to_bin(pixels)  
            bin_data2 += r
            bin_data2 += g
            bin_data2 += b
    # diff = find_diff(bin_data1, bin_data2)

    for i in range(len(bin_data1)):
        if bin_data1[i] != bin_data2[i]:
            diff += bin_data2[i]

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
    return

main()