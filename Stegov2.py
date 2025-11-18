from PIL import Image


#convert text to binary to use later for embedding in the image

def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

#function to find the greatest common divisor

def gcd(x,y):
    while y != 0:
        x, y=y, y % x
    
    return x

#get the image the user wanna use to embed data to 

def get_image(location):
    img = Image.open(location).convert("RGB")
    pixels = img.load()
    w, h = img.size
    return img, pixels, w, h

def encode_image(image_location, msg):
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
            print("Hidden message:", hidden_msg)
            continue
        elif choice == 'q':
            print("Quitting the program.")
            break
        else:
            print("Invalid choice. Please choose 'e', 'd', or 'q'.")
            continue

if __name__ == '__main__':
    #main()
    
    out = encode_image("test.jpg", "fuck you!!!")
    out.save("encoded.png")
    decoded_message = decode_image("encoded.png")
    print(decoded_message)