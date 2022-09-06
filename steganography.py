import numpy as np
import cv2

NUM_LSB = 3  #8

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
    secret_msg += '########'  #Adding more than what we are looking for to be decoded
    dataIndex = 0  
    secret_msg = msg_to_bin(secret_msg)
    dataLen = len(secret_msg)   
     
    for values in img: # values is rows  
        for pixels in values:  # pixels is a column in a row
            # converting RGB values to binary format  
            r, g, b = msg_to_bin(pixels)
            # modifying the LSB only if there is data remaining to store  
            if dataIndex < dataLen:
                pixels[0] = int(r[:len(r)-(NUM_LSB)] + secret_msg[dataIndex:dataIndex+NUM_LSB], 2) 
                print("r: " + str(r))
                print("pixels[0]: " + str(msg_to_bin(pixels[0])))
                dataIndex += NUM_LSB
            if dataIndex < dataLen:   
                pixels[1] = int(g[:len(g)-(NUM_LSB)] + secret_msg[dataIndex:dataIndex+NUM_LSB], 2)  
                dataIndex += NUM_LSB
                print("g: " + str(g))
                print("pixels[1]: " + str(msg_to_bin(pixels[1])))
            if dataIndex < dataLen:   
                pixels[2] = int(b[:len(b)-(NUM_LSB)] + secret_msg[dataIndex:dataIndex+NUM_LSB], 2)  
                dataIndex += NUM_LSB
                print("b: " + str(b))
                print("pixels[2]: " + str(msg_to_bin(pixels[2])))
            if dataIndex >= dataLen:  
                break  
    return img  

def show_data(img):  
    bin_data = ""  
    for values in img:  
        for pixels in values:  
            # converting the Red, Green, Blue values into binary format  
            r, g, b = msg_to_bin(pixels)  
            bin_data += r[-NUM_LSB:] 
            bin_data += g[-NUM_LSB:]   
            bin_data += b[-NUM_LSB:]  
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
    #print(len(img[0]))
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
    m = ""
    for values in img: # values is rows  
        for pixels in values:  # pixels is a column in a row
            # converting RGB values to binary format  
            r, g, b = msg_to_bin(pixels)
            # modifying the LSB only if there is data remaining to store
            
            m += r[-NUM_LSB:] + g[-NUM_LSB:] + b[-NUM_LSB:]
            '''if dataIndex < dataLen:
                pixels[0] = int(r[:len(r)-(NUM_LSB)] + secret_msg[dataIndex:dataIndex+NUM_LSB], 2) 
                print("r: " + str(r))
                print("pixels[0]: " + str(msg_to_bin(pixels[0])))
                dataIndex += NUM_LSB
            if dataIndex < dataLen:   
                pixels[1] = int(g[:len(g)-(NUM_LSB)] + secret_msg[dataIndex:dataIndex+NUM_LSB], 2)  
                dataIndex += NUM_LSB
                print("g: " + str(g))
                print("pixels[1]: " + str(msg_to_bin(pixels[1])))
            if dataIndex < dataLen:   
                pixels[2] = int(b[:len(b)-(NUM_LSB)] + secret_msg[dataIndex:dataIndex+NUM_LSB], 2)  
                dataIndex += NUM_LSB
                print("b: " + str(b))
                print("pixels[2]: " + str(msg_to_bin(pixels[2])))
            if dataIndex >= dataLen:  
                break'''  
    #print(m[32])
    #return img  
    #text = show_data(img)
    return m[0:33]  

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