# COSC 480B HW 1 Part 1
# Group Members: Diego Abanto, Jin Sohn, Sara Alam

import numpy as np
import cv2

NUM_LSB = 3

key = "H"

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

# hide the data in the image
def hide_data(img, secret_msg):
    shift = 0
    if(key == "H"):
        shift = str(len(img))
    else:
        shift = str(len(img[0]))      
    secret_msg += '##########'  #Adding more than what we are looking for to be decoded
    dataIndex = 0  
    secret_msg = msg_to_bin(secret_msg)
    dataLen = len(secret_msg)   
    mod = 0 # index of the pixel inside a cell, one of r, g or b
    k = 0  # index in the shift number, keeps track of which digit is being used to shift

    for i in range(len(img)):
        k = (k+1) % len(shift) # update k to move to the next digit in the shift number
        values = img[i]
        j = 0
        while j < len(values):
            pixels = values[j]  
            # converting RGB values to binary format  
            px = msg_to_bin(pixels[mod])

            # modifying the LSB only if there is data remaining to store
            if dataIndex < dataLen: 
                pixels[mod] = int(px[:len(px)-(NUM_LSB)] + secret_msg[dataIndex:dataIndex+NUM_LSB], 2) 
                dataIndex += NUM_LSB

            if dataIndex >= dataLen:  
                break

              
            x = int(shift[k]) # current shift value
            if (j+int(x/3)) > len(values):
                break
            if x == 0:
                x = 1
            # update mod and j    
            j += int(x/3) # because j is the cell number and x indicates pixel number
            mod += x % 3
            if mod >= 3:
                j += 1
                mod = mod % 3

        if dataIndex >= dataLen:  
            break 

    return img  

def show_data(img):
    shift = 0
    if(key == "H"):
        shift = str(len(img))
    else:
        shift = str(len(img[0]))  
    bin_data = ""
    
    mod = 0
    k = 0  # index in shift
    for i in range(len(img)):
        k = (k+1) % len(shift) # update k
        values = img[i]
        j = 0
        while j < len(values):
            pixels = values[j]  
            # converting RGB values to binary format  
            px = msg_to_bin(pixels[mod])
            #print(px)
            bin_data += px[-NUM_LSB:]
            
            x = int(shift[k]) # current shift value
            if (j+int(x/3)) > len(values):
                break
            if x == 0:
                x = 1    
            j += int(x/3)
            mod += x % 3
            if mod >= 3:
                j += 1
                mod = mod % 3
    """ for values in img:  
        for pixels in values:  
            # converting the Red, Green, Blue values into binary format  
            r, g, b = msg_to_bin(pixels)  
            bin_data += r[-NUM_LSB:] 
            bin_data += g[-NUM_LSB:]   
            bin_data += b[-NUM_LSB:]   """
    # splitting by 8-bits  
    allBytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]  
    # converting from bits to characters  
    decodedData = ""  
    for bytes in allBytes:  
        decodedData += chr(int(bytes, 2))
        # checking if we have reached the delimiter which is "#####"  
        if decodedData[-5:] == "#####":  
            break 
    # removing the delimiter to display the actual hidden message  
    return decodedData[:-5]

def encodeText():  
    img_name = input("Enter image name (with extension): ")  
    img = cv2.imread(img_name)
    data_name = input("Enter the name of the file that has your message to encode: ")
    f = open(data_name, "r")
    data = f.read()
    f.close()
    file_name = input("Enter the name of the new encoded image (with extension): ")  
    encodedImage = hide_data(img, data)  
    cv2.imwrite(file_name, encodedImage)  

def decodeText():  
    # reading the image containing the hidden image  
    img_name = input("Enter the name of the Steganographic image that has to be decoded (with extension): ")  
    img = cv2.imread(img_name)  # reading the image using the imread() function  
    text = show_data(img)
    return text  

def steganography():  
    n = int(input("1. Encode the data \n2. Decode the data \n Select the option: "))  
    if (n == 1):  
        print("\nEncoding...")  
        encodeText()  
    elif (n == 2):  
        print("\nDecoding...")  
        print("Decoded message is: " + decodeText()) 
    else:  
        raise Exception("Inserted value is incorrect!")  
  
steganography()