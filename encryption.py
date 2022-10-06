import os
import base64
import maskpass
import pyperclip
from database import PMdatabase
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


class Baddy:
    def __init__(self) -> None:
        self.db = PMdatabase()

    def signup(self):
        username = input("Enter your User ID/Name: \n[This ID/Name will only used for differentiating you from the other users. It'll not be used for encryption]\n")

        self.gen_master_password(username)

    def gen_master_password(self, username):
        #master salt
        msalt = os.urandom(16)
        self.db.insert_data(username, msalt)

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
                self.db.insert_master_password(encrypted_master_password, username)
                self.db.create_username_table(username)
                print("Sign Up successfull!")
            else:
                print("[entries didn't match, try again]") 

    def login(self):
        logged = False
        while logged != True:
            username = input("Enter your User ID/Name: ")

            row = self.db.cursor.execute(f"SELECT * FROM user WHERE username = '{username}'").fetchone()
            if(row == None):
                print(f"[No user with username: '{username}' found in database, try again]")
            else:
                pass_check = False
                while pass_check != True:
                    msalt = row[1]

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

                    if encrypted_master_password != row[2]:
                        print("[Incorrect UserName or MasterPassword, try again]")
                    else:
                        pass_check = True

                print(f"You're successfully Logged In!\nWelcome {username}")
                logged = True

        self.activeUser = row
        self.fernet_obj= Fernet(base64.urlsafe_b64encode(self.activeUser[2]))

    def save_passwords(self):
        username = self.activeUser[0]

        name_of_site = input("Enter the name of site: ")
        url = input("Enter the url of site: ")

        salt= os.urandom(16)
        query = f"""INSERT INTO {username}(name_of_site, salt, url) VALUES(?, ?, ?)"""
        
        self.db.cursor.execute(query, (name_of_site, salt, url))
        self.db.connection.commit()

        row = self.db.cursor.execute(f"SELECT * FROM {username}").fetchone()

        confirm_password_match = False
        while confirm_password_match != True:

            site_password = maskpass.askpass("Enter the password of site: ").encode()
            confirm_site_password = maskpass.askpass("Confirm password: ").encode()
            

            if site_password == confirm_site_password:
                encrypted_password = self.fernet_obj.encrypt(site_password)

                confirm_password_match = True

                query = f"""UPDATE {username} SET password = ? WHERE name_of_site = '{name_of_site}'"""
                self.db.cursor.execute(query, (encrypted_password,))
                self.db.connection.commit()
                
                row = self.cursor.execute(f"SELECT * FROM {username} WHERE name_of_site = '{name_of_site}'").fetchone()
            else:
                print("[entries didn't match, try again]")

        print(f"Succesfully saved your {name_of_site} password")

    def get_password(self):
        username = self.activeUser[0]

        while True:
            name_of_site = input("Enter name of site which password you want: ")

            row = self.db.cursor.execute(f"""SELECT password FROM {username} WHERE name_of_site = '{name_of_site}'""").fetchone()
            if row != None:
                break
            else:
                name_of_site = input("[Invalid Entry] retry: ")

        pyperclip.copy(self.fernet_obj.decrypt(row[0]).decode())
        print("[Your password is copied to your clipboard!]")  
    
    def edit_info(self):
        username = self.activeUser[0]
        while True:
            name_of_site = input("Enter name of site of which you want to edit info: ")

            row = self.db.cursor.execute(f"""SELECT password FROM {username} WHERE name_of_site = '{name_of_site}'""").fetchone()
            if row != None:
                break
            else:
                name_of_site = input("[Invalid Entry] retry: ")

            
        print("""
        (u)Change url of the site.
        (p)change password for the site.""")

        field = input("Enter your choice: ")

        if(field == 'u'):
            new_url = input("Enter new url of the site: ")
            self.db.cursor.execute(f"""UPDATE {username} SET url = '{new_url}' WHERE name_of_site = '{name_of_site}'""")

        elif(field == 'p'):
            confirm_password_match = False
            while confirm_password_match != True:

                site_password = maskpass.askpass("Enter the password of site: ").encode()
                confirm_site_password = maskpass.askpass("Confirm password: ").encode()
                

                if site_password == confirm_site_password:
                    encrypted_password = self.fernet_obj.encrypt(site_password)

                    confirm_password_match = True

                    query = f"""UPDATE {username} SET password = ? WHERE name_of_site = '{name_of_site}'"""
                    self.db.cursor.execute(query, (encrypted_password,))
                    self.db.connection.commit()
                    break
                else:
                    print("[entries didn't match, try again]")

        elif(field == 'p'):
                return
        else:
            print("[Invalid choice")

        print(f"Succesfully changed your {name_of_site} password")


