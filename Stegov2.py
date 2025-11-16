from PIL import Image
import hashes

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
    print(y, x)

#get the image the user wanna use to embed data to 

def get_image(loc):
    img = Image.open(loc, 'r')
    pix_val = list(img.getdata())
    print(pix_val)

# Add logic to embed data in image:



if __name__ == '__main__':
    gcd(600, 400)
    get_image("test2.png")
    pass #main()