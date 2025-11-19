import Encryption

while True:
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