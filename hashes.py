from AES_Python import AES
import os


def padding(msg):
    padding_length = 16 - len(msg) % 16
    padding = ([padding_length] * padding_length)
    return msg + padding

def unpadding(msg):
    padding_length = msg[-1]
    if padding_length < 1 or padding_length > 16:
        raise ValueError("Invalid padding encountered")
    return msg[:-padding_length]

    
def load_key():
    if not os.path.exists(".key"):
        key = os.urandom(32)
        iv = os.urandom(16)
        with open(".key", "wb") as key_file:
            key_file.write(key + iv)
    elif os.path.getsize(".key") != 48:
        key = os.urandom(32)
        iv = os.urandom(16)
        with open(".key", "wb") as key_file:
            key_file.write(key + iv)
    elif os.path.getsize(".key") == 48:
        with open(".key", "rb") as key_file:
            data = key_file.read()
            key = data[:32]
            iv = data[32:]
    return key, iv


def encrypt_data(msg, key, iv):
    load_key()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        ciphertext = cipher.encrypt(padding(msg))
        encocded_key = key.hex()
        encoded_iv = iv.hex()
        return ciphertext, encocded_key, encoded_iv
    except Exception as e:
        print("Encryption error:", e)
        return None, None, None
            
            
    
def decrypt_data(msg):
     pass