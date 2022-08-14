import os
import maskpass
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#to salt creates random character array size in bit
salt = os.urandom(16)
dict = {
    "salt":salt
}

with open("salt1.key",'wb') as f:
    f.write(salt)

# with open("multisalt.json",'wb') as f:
#     json.dump(dict,f)

password = b"rathod.shantanu"

#function
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000
)

#conversion of password
key = base64.urlsafe_b64encode(kdf.derive(password))

#making fernet object
f = Fernet(key)

#msg
msg = b'My Dirty Secrets!'

token = f.encrypt(msg)

user_in = maskpass.askpass("Enter your master password: ", mask='*')

with open("salt1.key",'rb') as f:
    salt_read = f.read()    

#verify
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt_read,
    iterations=390000
)

key_new = base64.urlsafe_b64encode(kdf.derive(password))

f_new = Fernet(key_new)

decrypted_msg = f_new.decrypt(token)
print("decrypted_msg: ", decrypted_msg.decode())