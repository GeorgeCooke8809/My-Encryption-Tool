def encrypt(plain_text: str, key: str, level: str):
    if key == "" and level != "Vernam":
        key = "L0"
    
    if level == "Directional Caesar":
        encrypted_text = level_one_convert(plain_text, key)
    elif level == "Vernam":
        encrypted_text = vernam_toggle(plain_text, key)
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

    if level == "Directional Caesar":
        plain_text = level_one_convert(encrypted_text, decryption_key)
    elif level == "Vernam":
        plain_text = vernam_toggle(encrypted_text, encryption_key)
    else:
        plain_text = level_two_convert(encrypted_text, decryption_key)

    return plain_text

def encrypt_alphabet(direction: str, amount: int):
    plain_alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,<>/;:'@][-_=+1234567890!£$%^&*()")

    amount = amount % 87
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
    """  
    Also called "Directional Caesar"

    PROCESS caesar convert (plain text, encryption key)
        SET direction = encryption key [0]
        SET magnitude = encryption key [1::]
        SET new alphabet = alphabet shifted magnitude in direction

        FOR letter in plain text:
            SET new letter = new alphabet [index(letter)]
            SET encrypted text = encrypted text + new letter

        PRINT encrypted text
    END
    """
    plain_alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,<>/;:'@][-_=+1234567890!£$%^&*()")

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
    """
    Also called "Directional Polyshift"

    PROCESS directional polyshift (plain text, encryption key)
        SET direction = encryption key [0]
        FOR index in length of plain text:
            SET key index = index MOD length(encryption key) - 1
            SET magnitude = key [key index]
            SET new alphabet = alphabet shifted direction by magnitude
            SET new letter = new alphabet [index(letter)]
            SET encrypted text = encrypted text + new letter
        PRINT encrypted text
    END
    """
    index = 0
    plain_alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,<>/;:'@][-_=+1234567890!£$%^&*()")

    encrypted_text = ""

    try:
        encryption_direction = key[0]

        if key_number.isnumeric():
            key_number = key[1:]
        else:
            key_number = "0"
    except:
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
    """
    PROCESS vernam toggle (plain text, encryption key)
        FOR index in length(plain text);
            SET key index = index MOD length(encryption key)
            SET key letter = key [key index]
            SET key value = binary(key letter index in alphabet)
            SET current letter = binary(plain text [index])
            SET new index = integer(key value XOR current letter)
            SET new letter = alphabet [new index]
            SET encrypted text = encrypted text + new letter
        PRINT encrypted text
    END
    """
    if key == "":
        key = "a"
    alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,<>/;:'@][-_=+1234567890!£$%^&*()")
    cypher = ""

    length_plain = len(plain)
    length_key = len(key)

    for i in range(length_plain):
        try:
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
            
        except:
            cypher = f"{cypher}{plain[i]}"

    return cypher