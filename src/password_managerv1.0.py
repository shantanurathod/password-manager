#create edit passwords
#use regex to set constraint for master password and email
#add email id for login
#use email to encrypt all files
#make loading bar and add colors to text
#use google drive to back up data

from hashlib import sha256
import mysql.connector as connector
import json
import os
import base64
import re
import maskpass
import pyperclip
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class DBHelper:
    def __init__(self) -> None:
        self.con = connector.connect(host='localhost', port='3306', user='root', password='b00b_mysqlbaby', database='passwordmanager_test')

        
class PasswordManager:

    login_salt = b'C\xb3\xb9\x97b\x87,\x183:\xef~\x02\x0b\xe56'
    regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    def __init__(self) -> None:
        print("""Welcome to PM!
                (1)Sign Up
                (2)Log in
                (q)Quit\n""")
        self.run()

    def run(self):
        choice = None        
        while choice != 'q':
            # os.system('cls')
            choice = input("\nEnter your choice: ")
            if choice == '1':
                self.signup()
            elif choice == '2':
                self.login()
                self.run_logged()
            elif choice == 'q':
                os.system('cls')
                print("Thank you for using PM!")                
            else:
                print("[Invalid choice]")    

    def run_logged(self):
        choice = None        
        while choice != 'q':
            # os.system('cls')
            print("""
                    (1)save passwords
                    (2)get passwords
                    (3)edit information
                    (q)Quit\n""")

            choice = input("\nEnter your choice: ")
            if choice == '1':
                self.save_passwords()
            elif choice == '2':
                self.get_password()
            elif choice == '3':
                self.edit_info()
            elif choice == 'q':
                print("[press q to confirm Quit program]")
            else:
                print("[Invalid choice]")              

    def load_database(self):
        if os.path.exists("data.json") and os.stat("data.json").st_size != 0:
            with open("data.json",'r') as f:
                database = json.loads(f.read())
        else:
            database = {}
        return database  

    def encrypt_json(password):
        salt = PasswordManager.login_salt

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length= 32,
            salt= salt,
            iterations=390000
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.decode()))

        fer = Fernet(key)

        with open('data.json','r') as f:
            data = f.read()

        encrypted_data = fer.encrypt(data)

        with open('data.txt','wb') as f:
            f.write(encrypted_data)

    def decrypt_json(password):
        if os.path.exists("data.json") and os.stat("data.json").st_size != 0:
            salt = PasswordManager.login_salt

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length= 32,
                salt= salt,
                iterations=390000
            )

            key = base64.urlsafe_b64encode(kdf.derive(password.decode()))

            fer = Fernet(key)

            with open('data.txt','rb') as f:
                encrypted_data = f.read()

            data = fer.decrypt(encrypted_data).decode()

            with open('data.json', 'w') as f:
                json.dumps(data,f)

    def login(self):
        logged = False
        while logged != True:
            Admin_name = input("Enter your User ID/Name: ")
            # Admin_email = input("Enter your email ID: ")
            
            # while self.valid_re(PasswordManager.regex_email,Admin_email) != True:
            #     Admin_email = input("[Invalid email]retype: ")

            try:
                os.chdir(Admin_name)
                # self.decrypt_json(Admin_email)
                logged = True
                print(f"You're successfully Logged In!\nWelcome {self.get_UserName()}")
            except:
                print("[Invalid User]")

    def valid_re(self,regex,expre):
        if(re.fullmatch(regex,expre)):
            return True
        else:
            return False

    def signup(self):
        Admin_name = input("Enter your User ID/Name: \n[This ID/Name will only used for differentiating you from the other users. It'll not be used for encryption]\n")
        os.mkdir(Admin_name)
        # Admin_email = input("Enter your email ID: ")
        # while self.valid_re(PasswordManager.regex_email,Admin_email) != True:
        #         Admin_email = input("[Invalid email]retype: ")

        self.gen_master_password()

    def get_UserName(self):
        Admin_name = os.path.basename(os.getcwd())
        return Admin_name

    def gen_master_password(self):
        #master salt
        msalt = os.urandom(16)

        #storing master salt
        with open('ms.key','wb') as f:
            f.write(msalt)

        confirm_password_match = False
        while confirm_password_match != True:
            #derive
            kdf = Scrypt(
                salt = msalt,
                length = 32,
                n = 2**14,
                r = 8,
                p = 1
            )
        
            #making master password
            encrypted_master_password = kdf.derive(maskpass.askpass("Enter your master password: ").encode())

            #storing encrypted_master_password
            with open('mp.key','wb') as f:
                f.write(encrypted_master_password)

            #confirm master password
            kdf = Scrypt(
                salt = msalt,
                length = 32,
                n = 2**14,
                r = 8,
                p = 1
            )
            
            if kdf.derive(maskpass.askpass("Confirm Password: ").encode()) == encrypted_master_password:
                confirm_password_match = True
                print("Sign Up successfull!")
            else:
                print("[passwords didn't match, try again]")    


    def save_passwords(self):
        database = self.load_database()
        name_of_site = input("Enter the name of site: ")

        database[f"{name_of_site}"] = {}

        salt_= os.urandom(16)
        salt_encode = str(base64.urlsafe_b64encode(salt_),'utf-8')
        # print(" salt_encode:",  salt_encode)
        
        database[f"{name_of_site}"]["salt"] = salt_encode
        database[f"{name_of_site}"]["url"] = input("Enter the url of site: ")

        confirm_password_match = False
        while confirm_password_match != True:
            kdf = Scrypt(
                salt=salt_,
                length = 32,
                n = 2**14,
                r = 8,
                p = 1
            )

            fernet_obj= Fernet(base64.urlsafe_b64encode(kdf.derive(maskpass.askpass("Enter your master password: ",mask="*").encode())))
            encrypted_password = fernet_obj.encrypt(maskpass.askpass("Enter the password of site: ").encode())

            kdf = Scrypt(
                salt=salt_,
                length = 32,
                n = 2**14,
                r = 8,
                p = 1
            )
            # fernet_obj2= Fernet(base64.urlsafe_b64encode(kdf.derive(maskpass.askpass("Enter your master password: ",mask="*").encode())))
            if fernet_obj.encrypt(maskpass.askpass("Enter the password of site: ").encode()) == encrypted_password:
                confirm_password_match = True
                database[f"{name_of_site}"]["password"] = str(encrypted_password,'utf-8')
            else:
                print("[passwords didn't match, try again]")

        # print("encrypted_password: ", encrypted_password)
        
        # self.dict["user_name"] = input("Enter  the user_name for site: ")
        # self.dict["email"] = input("Enter  the email for site: ")

        # print(database)

        with open("data.json",'w') as f:
            json.dump(database,f)


        print(f"Succesfully saved your {name_of_site} password")

    def get_password(self):
        database = self.load_database()
        if os.path.exists("data.json") and os.stat("data.json").st_size != 0:
            name_of_site = input("Enter name of site which password you want: ")
            while name_of_site in database !=False:
                name_of_site = input("[Invalid Entry]retype: ")

            salt_ = base64.urlsafe_b64decode(bytes(database[f"{name_of_site}"]["salt"],'utf-8'))

            kdf = Scrypt(
                salt=salt_,
                length = 32,
                n = 2**14,
                r = 8,
                p = 1
            )

            fernet_obj= Fernet(base64.urlsafe_b64encode(kdf.derive(maskpass.askpass("Enter your master password: ",mask="*").encode())))
            pyperclip.copy(fernet_obj.decrypt(bytes(database[f"{name_of_site}"]["password"],'utf-8')).decode())
            print("[Your password is copied to your clipboard!]")    
        else:
            print("[Your database is empty]")    

    def edit_info(self):
        database = self.load_database()
        if os.path.exists("data.json") and os.stat("data.json").st_size != 0:
            site_name = input("Enter the name of site: ")
            while not (site_name in database.keys()) :
                site_name = input("[Invalid Entry]retype: ")
        
            print("""
            (u)Change url of the site.
            (p)change password for the site.""")

            field = input("Enter your choice: ")

            if(field == 'u'):
                new_url = input("Enter new url of the site: ")
                try:
                    database[site_name]["url"] = new_url
                    print("[Successfully updated your info]") 
                except:
                    print("[Incorrect site name}]")
            elif(field == 'p'):
                try:
                    salt_= os.urandom(16)
                    salt_encode = str(base64.urlsafe_b64encode(salt_),'utf-8')

                    database[f"{site_name}"]["salt"] = salt_encode

                    confirm_password_match = False
                    while confirm_password_match == False:
                        kdf = Scrypt(
                            salt=salt_,
                            length = 32,
                            n = 2**14,
                            r = 8,
                            p = 1
                        )

                        fernet_obj= Fernet(base64.urlsafe_b64encode(kdf.derive(maskpass.askpass("Enter your master password: ",mask="*").encode())))
                        encrypted_password = fernet_obj.encrypt(maskpass.askpass("Enter the new password of site: ").encode())

                        # kdf = Scrypt(
                        #     salt=salt_,
                        #     length = 32,
                        #     n = 2**14,
                        #     r = 8,
                        #     p = 1
                        # )
                        # fernet_obj2= Fernet(base64.urlsafe_b64encode(kdf.derive(maskpass.askpass("Enter your master password: ",mask="*").encode())))

                        confirm_password = fernet_obj.encrypt(maskpass.askpass("Confirm password: ").encode())

                        print("encrypted pass: ", encrypted_password, fernet_obj.decrypt(encrypted_password))
                        print("confirmed pass: ", confirm_password, fernet_obj.decrypt(confirm_password))

                    

                        # if fernet_obj.encrypt(maskpass.askpass("Confirm password: ").encode()) == encrypted_password:
                        #     confirm_password_match = True
                        #     database[f"{site_name}"]["password"] = str(encrypted_password,'utf-8')
                        # else:
                        #     print("[passwords didn't match, try again]")

                    # with open("data.json",'w') as f:
                    #     json.dump(database,f)

                    print(f"Succesfully saved your {site_name} password")

                except Exception as e:
                    print(e)
                    print("\n[Incorrect site name}]")
            else:
                print("[Invalid choice")

def main():
        PM = PasswordManager()

if __name__ == '__main__':
    main()