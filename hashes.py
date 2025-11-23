from AES_Python import AES
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
    key, iv = load_key()  # Use the stored IV from the file
    try:
        padded_msg = padding(msg)
        encoded_key = key.hex()
        encoded_iv = iv.hex()
        
        # Try passing IV as bytes instead of hex string
        #cipher = AES(running_mode="CBC", key=key.hex(), iv=iv.hex())
        
        # Alternative: try without specifying IV to see if library handles it differently
        cipher = AES(running_mode="CBC", key=key.hex())
        # cipher.iv = iv.hex()  # Set IV separately if supported
        
        ciphertext = cipher.enc(data_string=padded_msg.hex())
        
        print("Encryption successful.")
        print("Encoded Key:", encoded_key)
        print("Encoded IV:", encoded_iv)
        print("Ciphertext:", ciphertext)
        return ciphertext, encoded_key, encoded_iv
    except Exception as e:
        print("Encryption error:", e)
        return None, None, None

def decrypt_data(ciphertext, key_hex, iv_hex):
    try:
        cipher = AES(running_mode="CBC", key=key_hex, iv=iv_hex)
        decrypted_hex = cipher.dec(data_string=ciphertext)
        decrypted_bytes = bytes.fromhex(decrypted_hex)
        unpadded_msg = unpadding(decrypted_bytes)
        return unpadded_msg.decode('utf-8')
    except Exception as e:
        print("Decryption error:", e)
        return None