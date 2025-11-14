from PIL import Image
import hashlib
import hashes

# -----------------------------
# Utility functions 
# -----------------------------
def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary_str):
    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)

# -----------------------------
# Key management
# -----------------------------
def generate_key():
    """Generate and save a sha256 key."""
    key = hashlib.sha256().digest()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("New encryption key generated and saved as secret.key")

def load_key():
    """Load the sha256 key."""
    try:
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print("No key found. Generating new one...")
        generate_key()
        return load_key()

# -----------------------------
# Steganography encode/decode
# -----------------------------
def encode_image(input_image, message, output_image):
    # convert to RGBA to handle alpha consistently
    img = Image.open(input_image).convert('RGBA')
    binary_msg = text_to_binary(message) + '1111111111111110'  # terminator
    pixels = img.load()
    data_index = 0
    total_bits = len(binary_msg)

    for y in range(img.height):
        for x in range(img.width):
            if data_index >= total_bits:
                img.save(output_image)
                print(f"Encrypted message hidden in {output_image}")
                return

            r, g, b, a = pixels[x, y]
            new_r, new_g, new_b = r, g, b

            # set LSB of R, G, B in order if bits remain
            for channel_idx in range(3):
                if data_index < total_bits:
                    bit = int(binary_msg[data_index])
                    if channel_idx == 0:
                        new_r = (r & ~1) | bit
                    elif channel_idx == 1:
                        new_g = (g & ~1) | bit
                    else:
                        new_b = (b & ~1) | bit
                    data_index += 1

            pixels[x, y] = (new_r, new_g, new_b, a)

    print("Message too long for this image!")

def decode_image(stego_image):
    img = Image.open(stego_image).convert('RGBA')
    pixels = img.load()
    binary_data = ''

    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            # read LSBs of R, G, B in same order used to encode
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

            if binary_data.endswith('1111111111111110'):
                # remove terminator and convert
                return binary_to_text(binary_data[:-16])
    return None

# -----------------------------
# Main logic
# -----------------------------
def main():
    choice = input("1. Encode\n2. Decode\nChoose: ")
    key = load_key()
    cipher = hashlib.sha256(key)

    if choice == '1':
        img = input("Enter image name (with extension): ")
        msg = input("Enter message: ")

        # Encrypt the message before encoding
        encrypted_msg = cipher.encrypt(msg.encode()).decode()
        out = input("Save as: ")
        encode_image(img, encrypted_msg, out)

    elif choice == '2':
        img = input("Enter encoded image name: ")
        encrypted_text = decode_image(img)
        if encrypted_text:
            try:
                decrypted_msg = cipher.decrypt(encrypted_text.encode()).decode()
                print("Decrypted hidden message:", decrypted_msg)
            except Exception:
                print("Failed to decrypt message. Wrong key?")
        else:
            print("No hidden message found.")

    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()