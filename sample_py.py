from hashlib import md5
from Cryptodome.Cipher import AES
from os import urandom

#check https://devrescue.com/python-encrypt-file-with-aes/

def derive_key_and_iv(password, salt, key_length, iv_length): #derive key and IV from password and salt.
    d = d_i = b''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + str.encode(password) + salt).digest() #obtain the md5 hash value
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size #16 bytes
    salt = urandom(bs) #return a string of random bytes
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write(salt)
    finished = False

    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:#final block/chunk is padded before encryption
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += str.encode(padding_length * chr(padding_length))
            finished = True
        out_file.write(cipher.encrypt(chunk))

def decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = chunk[-1]
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(bytes(x for x in chunk))


password = '12345' #for test purposes only -- shouldn't be something this simple

with open('/Users/vedantchauhan/Downloads/1F-01-22261-1C CYP11B2.svs', 'rb') as in_file, open('/Users/vedantchauhan/Downloads/1F-01-22261-1C CYP11B2-out.svs', 'wb') as out_file:
    encrypt(in_file, out_file, password)

#with open('/Users/vedantchauhan/Downloads/ANON2LTHVG1H2_1_1-out.ndpi', 'rb') as in_file, open('/Users/vedantchauhan/Downloads/ANON2LTHVG1H2_1_1-decrypted.ndpi', 'wb') as out_file:
    #decrypt(in_file, out_file, password)