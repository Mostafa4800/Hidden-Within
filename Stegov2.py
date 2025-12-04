from PIL import Image
from hashes import encrypt_data, decrypt_data


def print_banner():
    """ 
    Most important part. Everyone knows that a great program has great art
    """
    banner = r'''
                                       /   \          
                                      /     \        
                                     /       \        
                                    /         \         
                                   /           \          
                                  /             \      
+--------------------------------------------------------------------------------------+ 
|######################################################################################|
|######################################################################################|
|                                                                                      |
|          _   _ _     _     _               __        ___ _   _     _                 |
|         | | | (_) __| | __| | ___ _ __     \ \      / (_) |_| |__ (_)_ __            |
|         | |_| | |/ _` |/ _` |/ _ \ '_ \ ____\ \ /\ / /| | __| '_ \| | '_ \           |
|         |  _  | | (_| | (_| |  __/ | | |_____\ V  V / | | |_| | | | | | | |          |
|         |_| |_|_|\__,_|\__,_|\___|_| |_|      \_/\_/  |_|\__|_| |_|_|_| |_|          |
|                                                                                      |
|######################################################################################|
|######################################################################################|
+--------------------------------------------------------------------------------------+'''
    print(banner)

#convert encoded text to binary to use later for embedding in the image

def text_to_binary(msg):
    """ 
    This is where the clear text message gets encrypted to AES and then converted
    to bytes then then gets formatted to 8-bit bytes.
    """
    #Calls the encrypt fuction
    ciphertext_hex = encrypt_data(msg)
    #Converts the Ciphertext from hexadecimal to bytes
    ciphertext = bytes.fromhex(ciphertext_hex)
    #Converts the bytes to 8-bit bytes
    return ''.join(format(byte,'08b') for byte in ciphertext)

#Function to find the greatest common divisor

def gcd(x,y):
    """ 
    This is where we use Euclid’s algorithm to find the greatest common divisor (GCD)
    of two integers. This means the largest number that divides both integers without leaving a
    remainder.
    """
    while y != 0:
        x, y=y, y % x
    return x

#get the image the user wanna use to embed data to 

def get_image(location):
    """ 
    This function finds the image location, loading the pixels of the image, and its hight and width.
    """
    img = Image.open(location).convert("RGB")
    pixels = img.load()
    w, h = img.size
    return img, pixels, w, h

def encode_image(image_location, msg):
    """ 
    Here we imbed the encypted 8-bit binary text into the image by 
    """
    binary = text_to_binary(msg)   # conveert message to binary
    bit_index = 0 # index to keep track

    img, pixels, w, h = get_image(image_location) # get image and its pixels
    pattern = gcd(w, h) # calculate the pattern using gcd

    for i in range(h): # iterate through height
        for j in range(w): # iterate through width

            # logic
            if ((i + 1) * (j + 1)) % pattern == 0: # position matches the pattern

                # check if we're out of bits
                if bit_index >= len(binary):
                    # end marker → red = 0
                    r, g, b = pixels[j, i]
                    pixels[j, i] = (0, g, b)
                    return img

                # read next bit
                bit = int(binary[bit_index])
                bit_index += 1

                # modify LSB so the color red
                r, g, b = pixels[j, i]
                r = (r & ~1) | bit
                pixels[j, i] = (r, g, b)
    return img  # return the image

def decode_image(image_location):
    img, pixels, w, h = get_image(image_location)
    binary_data = []
    pattern = gcd(w, h) # calculate the pattern using gcd

    for i in range(h): # iterate through height
        for j in range(w): # iterate through width
            if ((i + 1) * (j + 1)) % pattern == 0: # position matches the pattern
                r, g, b = pixels[j, i]
                if r == 0:
                    
                    if not binary_data:
                        return ''
                    
                    list_of_bytes = [''.join(str(b) for b in binary_data[i:i+8]) for i in range(0, len(binary_data), 8)]
                    return ''.join(chr(int(byte, 2)) for byte in list_of_bytes if len(byte) == 8)
                binary_data.append(r & 1)

                
                
def main():
    print_banner()
    print("Steganography using GCD Pattern")
    while True:
        choice = input("Choose (e)ncode, (d)ecode or (q)uit: ").lower()
        if choice == 'e':
            image_location = input("Enter image file path: ")
            msg = input("Enter message to hide: ")
            encoded_img = encode_image(image_location, msg)
            output_path = input("Enter output image file path: ")
            encoded_img.save(output_path)
            print(f"Message encoded and saved to {output_path}")
            continue
        elif choice == 'd':
            image_location = input("Enter image file path: ")
            hidden_msg = decode_image(image_location)
            decrypted_msg = decrypt_data(hidden_msg)
            print("Hidden message:", decrypted_msg)
            continue
        elif choice == 'q':
            print("Quitting the program.")
            break
        else:
            print("Invalid choice. Please choose 'e', 'd', or 'q'.")
            continue

if __name__ == '__main__':
    main()
    
    #out = encode_image("test.jpg", "fuk you!!!")
    #out.save("encoded.png")
    #decoded_message = decode_image("encoded.png")
    #print(decoded_message)