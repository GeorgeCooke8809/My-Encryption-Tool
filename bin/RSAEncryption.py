import random
import math

def generate_keys(min_prime: int = 3, max_prime: int = 997):
    """
    This function is used to generate the keys later used in encryption.
    It takes in the minimum and maximum prime number to be used for the generation of the keys and defaults them to 
    a minimum of 3 and a maximum of 997.
    """

    prime_1 = 0
    prime_2 = 0
    while prime_1 == prime_2: # Triggers an infinite loop for if the prime numbers are the same.
        while not is_prime(prime_1):
            prime_1 = random.randint(min_prime, max_prime) # Generates a random prime number - Keep private

        while not is_prime(prime_2):
            prime_2 = random.randint(min_prime, max_prime) # Keep private

    n = prime_1 * prime_2 # This will be shared publicly
    phi_of_n = (prime_1 - 1) * (prime_2 - 1) # Keep Private

    public_key = random.randint(2+1, phi_of_n-1)

    while math.gcd(public_key, phi_of_n) != 1: # This repeats infinitely until the greatest common divisor of the public key and phi_of_n is 1
        public_key = random.randint(2+1, phi_of_n-1)

    private_key = 0

    while (public_key * private_key) % phi_of_n != 1: # Repeats infinitely by iterating through every number until it finds one where when the product of the public and private keys modded by phi of n is 1
        private_key += 1

    return (public_key, n, private_key) # Returns all of the keys for processing and later use.
            

def encrypt(text: str, public_key: int, n: int):
    """
    This function encrypts the data that is inputted into it (text) with the public key and value for n that is inputted into it.
    """

    alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,<>/;:'@][-_=+1234567890!£$%^&*()]")
    encrypted = ""

    for i in text:# Iterates through every character in the plain text separately
        try:
            char_index = alphabet.index(i)
            encrypted_char_index = (char_index ** public_key) % n # Puts the character index to the power of the public key and then mods it by n to get the cypher character
            encrypted = f"{encrypted}{encrypted_char_index} " # Compiles all of the cypher characters together
        except: pass # Adds no cypher if the plain text letter is not in the available alphabet

    return encrypted

def decrypt(cypher: str, private_key: int, n: int):
    """
    This function is used to decrypt teh cypher text inputted into it (Format: "1234 1234 1234 1234") using the private key and 
    value for n provided.
    """

    alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,<>/;:'@][-_=+1234567890!£$%^&*()")
    cypher = cypher.split()
    plain_text = ""

    for cypher_char in cypher: # Iterates through every character in the cypher separately
        cypher_char = int(cypher_char)

        plain_char_index = (cypher_char**private_key) % n # Puts the cypher character to the power of the private keys then mods it by n to get the index of the plain text character

        plain_char = alphabet[plain_char_index] # Gets the letter corresponding the plain text index
        plain_text = f"{plain_text}{plain_char}" # Compiles all of the plain text characters into a string

    return plain_text

def is_prime(number):
        """
        This function is used in the generation of the keys (the first function) to check if a number is prime.
        """

        if number <= 1:
            return False
        else:
            for i in range(2, int((number/2))+1):
                if number % i == 0:
                    return False
                
        return True