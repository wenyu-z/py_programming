# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 15:20:01 2016

@author: WZhao10
"""

#%% first test with text

from Crypto.Cipher import AES

# Encryption
key = '\xba\xcb\xaa\xd5\x9f\x05\xbf\x08VD\xb3\x91\xac\xb3L;\x9d\xc4\x1diHy*\x00\x19\x16QP\x1c\x82\x907'
plain_text = "1357510020002"

# Define key, AES mode and IV
encryption_suite = AES.new(key, AES.MODE_CFB, 'This is an IV456')
cipher_text = encryption_suite.encrypt(plain_text)

# Decryption
decryption_suite = AES.new(key, AES.MODE_CFB, 'This is an IV456')
decipher_text = decryption_suite.decrypt(cipher_text)



#%%

from Crypto.Cipher import AES
from hashlib import sha256 as SHA256
#from Crypto.Hash import SHA256, SHA512
import os, random, struct

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
                
def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        
        data = []
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
                
                data += [decryptor.decrypt(chunk)]
            outfile.truncate(origsize)
    return data
            

password = 'App254anyone?'

h = SHA256(password)

key2 = h.digest()

dirnow = 'dir_here'
filena = 'original_filename'
filenb = 'encrypted_filename'
filenc = 'decrypted_filename'

encrypt_file(key2, os.path.join(dirnow, filena), out_filename=None, chunksize=64*1024)
data = decrypt_file(key2, os.path.join(dirnow, filenb), out_filename=os.path.join(dirnow, filenc), chunksize=64*1024)
datalist = data[0].split('\r\n')

#%%
from Crypto.Cipher import AES
from hashlib import sha256 as SHA256
import os, random, struct

password = 'App254anyone?'

h = SHA256(password)

key = h.digest()

iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
encryptor = AES.new(key, AES.MODE_CBC, iv)
    
dirnow = 'dir_here'
filena = 'original_filename'

with open(os.path.join(dirnow, filena)) as f:
    data = f.readlines()
f.close()

cipher_data = [encryptor.encrypt(k) if len(k)%16==0 else encryptor.encrypt(k+' '*(16 - len(k)%16)) for k in data]

filenb = 'encrypted_filename'
with open(os.path.join(dirnow, filenb), "w+") as ff:
    line = ff.writelines(cipher_data)
ff.close()

with open(os.path.join(dirnow, filenb)) as ff_read:
    cipher_data_read = ff_read.read()

decryptor = AES.new(key, AES.MODE_CBC, iv)
decipher_data = [decryptor.decrypt(k) for k in cipher_data_read]




