from math import gcd
import random

def generate_e(phi_n):
    e = 2
    list = []
    while e < phi_n:
        m = gcd(e, phi_n)
        if m == 1:
            list.append(e)
        e = e + 1
    e = random.choice(list)
    return e

def generate_d(e, phi_n):
    d = 1
    r = (d*e)%phi_n
    while r != 1:
        d = d+1
        r = (d*e)%phi_n
    return d

def encode(message, key):
    words = message.split(" ")
    encryption = ""
    encrypted_words = []
    for i in words:
        word = encrypt_word(i, key)
        encrypted_words.append(word)
    for j in encrypted_words:
        encryption = encryption + str(j) + " "
    return encryption

def encrypt_word(word, key):
    encrypted_values = []
    values = []
    n, e = key
    encryption = ""
    for i in word:
        x = ord(i)
        values.append(x)
    for j in values:
        c = (j ** e) % n
        encrypted_values.append(c)
    for k in encrypted_values:
        encryption = encryption + str(k) + " "
    return encryption

def decipher(message, key):
    numbers = message.split("  ")
    original = ""
    decoded = []
    for i in numbers:
        pal = decipher_number(i, key)
        decoded.append(pal)
    for j in decoded:
        original = original + str(j) + " "
    return original

def decipher_number(num, key):
    list_numbers_decrypted = []
    list_numbers = []
    n, d = key
    decoded = ""
    numbers = num.split(" ")
    for i in numbers:
        if(i != ''):
            x = int(i)
            list_numbers.append(x)
    for j in list_numbers:
        m = (j ** d) % n
        list_numbers_decrypted.append(m)
    for k in list_numbers_decrypted:
        letter = chr(k)
        decoded = decoded + str(letter)
    return decoded

def generate_keys():
    p = 239
    q = 103
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = generate_e(phi_n)
    d = generate_d(e, phi_n)
    return (n, e), (n, d)

pub_key, priv_key = generate_keys()
msg = input("msg: ")
enmsg = encode(msg, pub_key)
print("encrypted msg: "+ str(enmsg))
demsg = decipher(enmsg, priv_key)
print("decrypted msg: ", str(demsg))