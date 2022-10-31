import os
from encryption import Baddy
    
class ConsoleUI:
    def __init__(self) -> None:
            self.baddy = Baddy()
            print("""Welcome to PM!
                    (1)Sign Up
                    (2)Log in
                    (q)Quit\n""")
            self.run()

    def run(self):
        choice = None        
        while choice != 'q':
            choice = input("\nEnter your choice: ")
            if choice == '1':
                self.baddy.signup()
                # self.run_logged()
            elif choice == '2':
                self.baddy.login()
                self.run_logged()
            elif choice == 'q':
                os.system('cls')
                print("Thank you for using PM!")                
            else:
                print("[Invalid choice]")    

    def run_logged(self):
        choice = None        
        while choice != 'q':
            print("""
                    (1)save passwords
                    (2)get passwords
                    (3)edit information
                    (q)Quit\n""")

            choice = input("\nEnter your choice: ")
            if choice == '1':
                self.baddy.save_passwords()
            elif choice == '2':
                self.baddy.get_password()
            elif choice == '3':
                self.baddy.edit_info()
                pass
            elif choice == 'q':
                print("[press q to confirm Quit program]")
            else:
                print("[Invalid choice]") 

if __name__ == '__main__':
    ui = ConsoleUI()

