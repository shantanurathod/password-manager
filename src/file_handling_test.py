import os
import json
import base64

salt = os.urandom(16)

ss = base64.urlsafe_b64encode(salt)

print("salt: ", salt)
print("salt_en: ", ss)
print("salt_en_utf: ", ss.decode('utf-8'))

dict = {
    "google.com": "hello world",
    "amazom.in": 89,
    "boolean_t": False,
    "pass":str(ss,'utf-8')
}

print("salt_de_utf", bytes(dict["pass"],'utf-8'))
print("salt_de: ", base64.urlsafe_b64decode(ss))

with open('dictest.json','w') as f:
    json.dump(dict,f)