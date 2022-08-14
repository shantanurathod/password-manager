import sys
from cryptography.fernet import Fernet

key = Fernet.generate_key()
print("key: ", key)
print("size of key: ", sys.getsizeof(key.decode()))
#print("size of key: ", sys.getsizeof(key), "in bytes")

msg = "Hello program nerd"

#creating object of class Fernet
Fr_obj = Fernet(key)

#encrypting
encrypted_msg = Fr_obj.encrypt(b'msg')

print('encrypted_msg: ', encrypted_msg)
print("size of encrypted msg: ", sys.getsizeof(encrypted_msg), "in bytes")
