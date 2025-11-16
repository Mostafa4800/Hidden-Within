import hashlib
from Stegov2 import text

def encrypt_message(message, key):
    h = hashlib.new('sha256')
    
    