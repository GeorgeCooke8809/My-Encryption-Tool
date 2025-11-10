def encrypt(plain_text: str, key: str, level: str):
    if key == "":
        key = "L0"
    
    if level == "Lvl. 1":
        encrypted_text = level_one_convert(plain_text, key)
    else:
        encrypted_text = level_two_convert(plain_text, key)

    return encrypted_text

def decrypt(encrypted_text: str, encryption_key: str, level: str):
    if level != "Vernam":
        if encryption_key == "":
            encryption_key = "L0"

        if encryption_key[0] == "R":
            decryption_key = "L" + encryption_key[1:]
        else:
            decryption_key = "R" + encryption_key[1:]

    if level == "Lvl. 1":
        plain_text = level_one_convert(encrypted_text, decryption_key)
    else:
        plain_text = level_two_convert(encrypted_text, decryption_key)

    return plain_text

def encrypt_alphabet(direction: str, amount: int):
    plain_alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ",", ".", "'", '"', ";", ":", "(", ")", "!", "$", "%", "&", "-", "_", "?", " "]

    amount = amount % 78
    new_alphabet = []
    new_alphabet.extend(plain_alphabet)

    if direction == "L":
        new_alphabet.extend(new_alphabet[0:amount])
        del(new_alphabet[0:amount])
    else:
        temp = new_alphabet[-amount:]
        temp.extend(new_alphabet)
        new_alphabet = temp
        del(new_alphabet[-amount:])

    return new_alphabet

def level_one_convert(text_in: str, key: str):
    plain_alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ",", ".", "'", '"', ";", ":", "(", ")", "!", "$", "%", "&", "-", "_", "?", " "]

    try:
        encryption_direction = key[0]
        encryption_amount = int(key[1:])

        encrypted_alphabet = encrypt_alphabet(encryption_direction, encryption_amount)

    except: # This will be triggered in the sandbox pages when the key is being typed in so that it does not crash when key is just "L" or "R"
        encrypted_alphabet = plain_alphabet

    encrypted_text = ""

    for i in text_in:
        try:
            position_original_alphabet = plain_alphabet.index(i)
            encrypted_char = encrypted_alphabet[position_original_alphabet]
            encrypted_text += encrypted_char
        except: # This will trigger if a character is not in the alphabet such as "%"
            encrypted_text += i

    return encrypted_text

def level_two_convert(text_in: str, key: str):
    index = 0
    plain_alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ",", ".", "'", '"', ";", ":", "(", ")", "!", "$", "%", "&", "-", "_", "?", " "]

    encrypted_text = ""

    if key not in ("L", "R"):
        encryption_direction = key[0]
        key_number = key[1:]
    else:
        encryption_direction = "L"
        key_number = "0"

    key_number_length = len(key_number)


    for i in text_in:
        current_key_index = index % key_number_length
        shift_amount = int(key_number[current_key_index])

        encrypted_alphabet = encrypt_alphabet(encryption_direction, shift_amount)

        try:
            position_original_alphabet = plain_alphabet.index(i)
            encrypted_char = encrypted_alphabet[position_original_alphabet]
            encrypted_text += encrypted_char
        except: # This will trigger if a character is not in the alphabet such as "%"
            encrypted_text += i
        
        index += 1

    return encrypted_text

def vernam_toggle(plain: str, key: str):
    alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,<>/;:'@][-_=+1234567890!£4%^&*()]")
    cypher = ""

    length_plain = len(plain)
    length_key = len(key)

    for i in range(length_plain):
        plain_index = alphabet.index(plain[i])
        if i > length_key-1:
            key_index = i % length_key
        else:
            key_index = i

        key_index = alphabet.index(key[key_index])

        plain_index = list(f'{plain_index:08b}')
        key_index = list(f'{key_index:08b}')

        letter = ""

        for i in range(8):
            temp = int(plain_index[i]) ^ int(key_index[i])
            letter = f"{letter}{temp}"

        new_index = int(letter, 2)
        cypher = f"{cypher}{alphabet[new_index]}"

    return cypher