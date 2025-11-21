import random
import math

def generate_keys(min_prime: int = 3, max_prime: int = 997):
    prime_1 = 0
    prime_2 = 0
    while prime_1 == prime_2:
        while not is_prime(prime_1):
            prime_1 = random.randint(min_prime, max_prime) # Keep private

        while not is_prime(prime_2):
            prime_2 = random.randint(min_prime, max_prime) # Keep private

    n = prime_1 * prime_2
    phi_of_n = (prime_1 - 1) * (prime_2 - 1) # Keep Private

    public_key = random.randint(2+1, phi_of_n-1)

    while math.gcd(public_key, phi_of_n) != 1:
        public_key = random.randint(2+1, phi_of_n-1)

    private_key = 0

    while (public_key * private_key) % phi_of_n != 1:
        private_key += 1

    return (public_key, n, private_key)
            

def encrypt(text: str, public_key: int, n: int):
    alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,<>/;:'@][-_=+1234567890!£4%^&*()]")
    encrypted = ""

    for i in text:
        try:
            char_index = alphabet.index(i)
            encrypted_char_index = (char_index ** public_key) % n
            encrypted = f"{encrypted}{encrypted_char_index} "
        except: pass

    return encrypted

def decrypt(cypher: int, private_key: int, n: int):
    alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,<>/;:'@][-_=+1234567890!£4%^&*()]")
    cypher = cypher.split()
    plain_text = ""

    for cypher_char in cypher:
        cypher_char = int(cypher_char)

        plain_char_index = (cypher_char**private_key) % n

        plain_char = alphabet[plain_char_index]
        plain_text = f"{plain_text}{plain_char}"

    return plain_text

def is_prime(number):
        if number <= 1:
            return False
        else:
            for i in range(2, int((number/2))+1):
                if number % i == 0:
                    return False
                
        return True