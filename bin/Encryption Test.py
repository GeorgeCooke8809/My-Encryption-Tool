import Encryption
import RSAEncryption

def file_1():
    print("1. Encrypt, \n2. Decrypt,")
    choice = input()

    text_in = input("Text In: ")
    key = input("Encryption Key: ")

    level_given = False
    while level_given == False:
        print("1. Directional Caesar \n2. Directional Polyshift \n3. Vernam Encryption")
        level = input()

        if level == "1":
            level = "Directional Caesar"
            level_given = True
        elif level == "2":
            level = "Directional Polyshift"
            level_given = True
        elif level == "3":
            level = "Vernam"
            level_given = True
        else:
            print("That is an invalid level. Try again.")

    if choice == "1": # Encrypt
        print(Encryption.encrypt(text_in, key, level))
    elif choice == "2": # Decrypt
        print(Encryption.decrypt(text_in, key, level))

def file_2():
    print(f"1. Generate Keys, \n2. Encrypt \n3. Decrypt")

    choice = int(input())

    if choice == 1:
        keys = RSAEncryption.generate_keys()
        print(f"Public Key: {keys[0]}\nN: {keys[1]}\nPrivate Key: {keys[2]}")
    elif choice == 2:
        text = input("Plain Text: ")
        public_key = int(input("Public Key: "))
        number = int(input("N: "))

        print(f"Cypher: {RSAEncryption.encrypt(text=text, public_key=public_key, n = number)}")
    elif choice == 3:
        cypher = input("Cypher: ")
        private_key = int(input("Private Key: "))
        n = int(input("N: "))

        print(f"Plain Text: {RSAEncryption.decrypt(cypher, private_key, n)}")


while True:
    print(f"Which library to test: \n1. Encryption.py\n2. RSAEncryption.py")
    choice = int(input())

    if choice == 1: file_1()
    elif choice == 2: file_2()