from math import gcd
import random

def generate_e(phi_n):
    # generate the public key
    e = 2
    le = []
    while e < phi_n:
        # put all the numbers that are lower than e in a list
        m = gcd(e, phi_n)
        if m == 1:
            le.append(e)
        e = e + 1
    # choose a random number from the list to be the public key
    e = random.choice(le)
    return e

def generate_d(e, phi_n):
    # generate private key using the public key
    d = 1
    r = (d*e)%phi_n
    # find a d so that the remainder of (e*d)/phi will be 1
    while r != 1:
        d = d+1
        r = (d*e)%phi_n
    return d

def encryption(msg, key):
    # split msg and them send every letter to
    # encryption with public key
    words = msg.split(" ")
    encrypted = ""
    encrypted_words = []
    for i in words:
        wrd = encrypt_word(i, key)
        encrypted_words.append(wrd)
    for j in encrypted_words:
        encrypted =encrypted + str(j) + " "
    return encrypted

def encrypt_word(wrd, key):
    #
    encrypted_values = []
    values = []
    n, e = key
    encrypted = ""
    for i in wrd:
        x = ord(i)
        values .append(x)
    for j in values:
        c = (j ** e) % n
        encrypted_values.append(c)
    for k in encrypted_values:
        encrypted = encrypted + str(k) + " "
    return encrypted

def decipher_text(msg, key):
    # split the message into words and then send each letter to be
    # encrypted
    nums= msg.split("  ")
    original = ""
    decoded= []
    for i in nums:
        pal = decipher_nums(i, key)
        decoded.append(pal)
    for j in decoded:
        original = original + str(j) + " "
    return original

def decipher_nums(num, key):
    # checks number with letter value in husky table
    decoded_num_list = []
    num_list = []
    n, d = key
    decoded = ""
    nums = num.split(" ")
    for i in nums:
        if(i != ''):
            x = int(i)
            num_list.append(x)
    for j in num_list:
        m = (j ** d) % n
        decoded_num_list.append(m)
    for k in decoded_num_list:
        letter = chr(k)
        decoded = decoded + str(letter)
    return decoded

def generate_keys():
    # choose 2 prime numbers and the calculate their multiply and their phi
    p = 239
    q = 103
    n = p * q
    phi_n = (p - 1) * (q - 1)
    # send to generate keys
    e = generate_e(phi_n)   # first public key
    d = generate_d(e, phi_n)    # private key
    return (n, e), (n, d)

pub_key, priv_key = generate_keys()
msg = input("msg: ")
enmsg= encryption(msg, pub_key)
print("encrypted msg is:", enmsg)
demsg = decipher_text(msg, priv_key)
print("decripted msg:", demsg)