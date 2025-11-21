from AES_Python import AES
import os
import Stegov2


aes = AES(r_mode="ECB", key=os.urandom(16))
iv = os.urandom(16)

def encrypt_data(text):
    pass
    

def decrypt_data(text):
    pass