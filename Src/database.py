import sqlite3

class PMdatabase:
    def __init__(self) -> None:
        self.connection = sqlite3.connect('PMdatabase.db')
        self.cursor = self.connection.cursor()
      
        tables = self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'""").fetchmany()

        emptyUserDB = True
        for table in tables:
            for name in table:
                if name == 'user':
                    emptyUserDB = False

        if emptyUserDB:        
            self.cursor.execute("""
            CREATE TABLE user(username VARCHAR(25), master_salt BLOB, master_password BLOB)
            """)
            self.connection.commit()
    
    def create_username_table(self, username):
        tables = self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'""").fetchmany()
        emptyUserNameTable = True
        for table in tables:
            for name in table:
                if name == username:
                    # print(name)
                    emptyUserNameTable = False

        if emptyUserNameTable:
            print(f"creating {username} table") 
            self.cursor.execute(f"""CREATE TABLE {username}(name_of_site varchar(50), username of site varchar(50), url varchar(200), password blob)""")
            self.connection.commit()

    def insert_data(self, username, msalt):
        usernames = self.cursor.execute("SELECT username FROM user")

        userNotExist = True
        for user_name in usernames:
            if user_name == username:
                print("[This user already exist]")
                userNotExist = False

        if userNotExist:
            query = f"""INSERT INTO user(username, master_salt) VALUES(?, ?)"""
            self.cursor.execute(query, (username, msalt))
            self.connection.commit()


    def insert_master_password(self, mp, username):
        query = """UPDATE user SET master_password = ? WHERE username = ?"""
        self.cursor.execute(query, (mp, username))
        self.connection.commit()