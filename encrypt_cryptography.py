# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 14:39:44 2016

@author: WZhao10
"""

#%% first test with text

from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher_suite = Fernet(key)

plain_text = "Make our size a strength"
cipher_text = cipher_suite.encrypt(plain_text)
decipher_text = cipher_suite.decrypt(cipher_text)


#%% logger data test: encrypt, key, decrypt 

import os
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher_suite = Fernet(key)

dirnow = 'dir_here'
filena = 'original_filename'

with open(os.path.join(dirnow, filena)) as f:
    data = f.readlines()
f.close()

cipher_data = [cipher_suite.encrypt(k)+'\n' for k in data]

filenb = 'encrypted_filename'
with open(os.path.join(dirnow, filenb), "w+") as ff:
#    [ff.write(k) for k in cipher_data]
    line = ff.writelines(cipher_data)
ff.close()

with open(os.path.join(dirnow, filenb)) as ff_read:
    cipher_data_read = ff_read.readlines()
        
decipher_data = [cipher_suite.decrypt(k) for k in cipher_data_read]

#key: IlOMRXSurzLcLVBuieKybswI_zIusknawAdLoVdML84=

#%% logger data test: decrypt with a given key

import os
from cryptography.fernet import Fernet

dirnow = 'dir_here'
filena = 'original_filename'

with open(os.path.join(dirnow, filena)) as f:
    data = f.readlines()
    
filenb = 'encrypted_filename'
with open(os.path.join(dirnow, filenb)) as ff:
    cipher_data = ff.readlines()
    
key = 'IlOMRXSurzLcLVBuieKybswI_zIusknawAdLoVdML84='
cipher_suite = Fernet(key)
decipher_data = [cipher_suite.decrypt(k) for k in cipher_data]



