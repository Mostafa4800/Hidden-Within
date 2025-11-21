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
    

class encrypt:


    def encrypt_data(msg):
        pass
    


class decrypt:
    
    def decrypt_data(msg):
        pass