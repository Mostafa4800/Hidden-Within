from Stegov2 import encode_image, decode_image
from crypto_utils import decrypt_data

def print_banner():
    """ 
    Most important part. Everyone knows that a great program has great art
    """
    banner = r'''
                                       /   \          
                                      /     \        
                                     /       \        
                                    /         \         
                                   /           \          
                                  /             \      
+--------------------------------------------------------------------------------------+ 
|######################################################################################|
|######################################################################################|
|                                                                                      |
|          _   _ _     _     _               __        ___ _   _     _                 |
|         | | | (_) __| | __| | ___ _ __     \ \      / (_) |_| |__ (_)_ __            |
|         | |_| | |/ _` |/ _` |/ _ \ '_ \ ____\ \ /\ / /| | __| '_ \| | '_ \           |
|         |  _  | | (_| | (_| |  __/ | | |_____\ V  V / | | |_| | | | | | | |          |
|         |_| |_|_|\__,_|\__,_|\___|_| |_|      \_/\_/  |_|\__|_| |_|_|_| |_|          |
|                                                                                      |
|######################################################################################|
|######################################################################################|
+--------------------------------------------------------------------------------------+'''
    print(banner)


def main():
    print_banner()
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
            decrypted_msg = decrypt_data(hidden_msg)
            print("Hidden message:", decrypted_msg)
            continue
        elif choice == 'q':
            print("Quitting the program.")
            break
        else:
            print("Invalid choice. Please choose 'e', 'd', or 'q'.")
            continue

if __name__ == '__main__':
    main()
    
    #out = encode_image("test.jpg", "fuk you!!!")
    #out.save("encoded.png")
    #decoded_message = decode_image("encoded.png")
    #print(decoded_message)