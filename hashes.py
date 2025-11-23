from Crypto.Cipher import AES as CryptoAES
import os

def padding(msg):
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    padding_length = 16 - len(msg) % 16
    padding_bytes = bytes([padding_length] * padding_length)
    return msg + padding_bytes

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

def encrypt_data(msg):
    key, iv = load_key()
    try:
        padded_msg = padding(msg)
        cipher = CryptoAES.new(key, CryptoAES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(padded_msg).hex()
        return ciphertext, key.hex(), iv.hex()
    except Exception as e:
        print("Encryption error:", e)
        return None, None, None

def decrypt_data(ciphertext_hex):
    key, iv = load_key()
    try:
        ciphertext = bytes.fromhex(ciphertext_hex)
        cipher = CryptoAES.new(key, CryptoAES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        print("Decrypted (raw):", decrypted)
        return unpadding(decrypted).decode("utf-8")
    except Exception as e:
        print("Decryption error:", e)
        return None