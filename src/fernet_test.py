#from sqlite3 import Timestamp
from cryptography.fernet import Fernet
import datetime
import time

# key = Fernet.generate_key()

# msg = b"This is a code red"

# f = Fernet(key)
# token = f.encrypt_at_time(msg,int(time.time()))

# with open("token1.txt",'wb') as f:
#     f.write(token)

# with open("key1.key",'wb') as f:
#     f.write(key)   
# Time_of_gen = f.extract_timestamp(token)

# print("Timestamp: ", datetime.datetime.fromtimestamp(Time_of_gen))

with open('key1.key','rb') as f:
    key = f.read()

fer = Fernet(key)

with open('token1.txt', 'rb') as f:
    token = f.read()

time_stamp = datetime.datetime.fromtimestamp(fer.extract_timestamp(token))
print("timestamp: ", time_stamp)
msg = fer.decrypt(token,540)

print("msg: ", msg.decode())