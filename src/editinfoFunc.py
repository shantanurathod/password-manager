def edit_info(self):
        database = self.load_database()
        if os.path.exists("data.json") and os.stat("data.json").st_size != 0:
            site_name = input("Enter the name of site: ")
            while f"{site_name}" in database !=True:
                site_name = input("[Invalid Entry]retype: ")
        
            print("""
            (u)Change url of the site.
            (p)change password for the site.""")

            field = input("Enter your choice: ")

            if(field == 'u'):
                new_url = input("Enter new url of the site: ")
                try:
                    database[site_name]["url"] = new_url 
                except:
                    print("[Incorrect site name}]")
            elif(field == 'p'):
                try:
                    salt_= os.urandom(16)
                    salt_encode = str(base64.urlsafe_b64encode(salt_),'utf-8')

                    database[f"{site_name}"]["salt"] = salt_encode

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
                    encrypted_password = fernet_obj.encrypt(maskpass.askpass("Enter the new password of site: ").encode())

                    kdf = Scrypt(
                        salt=salt_,
                        length = 32,
                        n = 2**14,
                        r = 8,
                        p = 1
                    )
                    fernet_obj2= Fernet(base64.urlsafe_b64encode(kdf.derive(maskpass.askpass("Enter your master password: ",mask="*").encode())))
                    if fernet_obj2.encrypt(maskpass.askpass("Confirm password: ").encode()) == encrypted_password:
                        confirm_password_match = True
                        database[f"{site_name}"]["password"] = str(encrypted_password,'utf-8')
                    else:
                        print("[passwords didn't match, try again]")

                    with open("data.json",'w') as f:
                        json.dump(database,f)

                    print(f"Succesfully saved your {site_name} password")

                except:
                    print("[Incorrect site name}]")
            else:
                print("[Invalid choice")