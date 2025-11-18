from PIL import Image


#convert text to binary to use later for embedding in the image

def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

#convert the embedded binary string pulled from the image to text

def binary_to_text(binary_str):
    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)

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



if __name__ == '__main__':
    out = encode_image("test.png", "Hello World")
    out.save("encoded.png")

    pass #main()