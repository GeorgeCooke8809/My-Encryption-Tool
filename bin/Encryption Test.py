import Encryption

while True:
    print("1. Encrypt, \n2. Decrypt,")
    choice = input()

    text_in = input("Text In: ")
    key = input("Encryption Key: ")

    level_given = False
    while level_given == False:
        print("1. Level 1 Encryption \n2. Level 2 Encryption\n3. Vernam Encryption")
        level = input()

        if level == "1":
            level = "Lvl. 1"
            level_given = True
        elif level == "2":
            level = "Lvl. 2"
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