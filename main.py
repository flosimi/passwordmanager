from cryptography.fernet import Fernet


class PasswordManager():
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, inital_values=None):
        self.password_file = path
        if inital_values is not None:
            for key, values in inital_values.items():
                self.add_password(key, values)

    def load_password_file(self, path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encoded()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    def get_password(self, site):
        return self.password_dict[site]

def main():
    password ={
        "email":"abcde",
        "facebook" :"password",
        "youtube":"adadawdas"
    }

    pm=PasswordManager()
    print("""
    (1) Create a new key
    (2) Load existing key
    (3) Create a new password file
    (4) Load existing password file
    (5) Add a new password
    (6) Get a password
    (q) Quit
    """)
    done =False
    while not done:
        choice = input("Enter your choice: ")
        if choice == "1":
            path = input("Enter path: ")
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter path: ")
            pm.load_key(path)
        elif choice == "3":
            path = input("Enter path: ")
            pm.create_password_file(path,password)
        elif choice =="4":
            path = input("Enter path: ")
            pm.load_password_file(path)
        elif choice =="5":
            site = input("Enter the site: ")
            password = input("Enter the password: ")
            pm.add_password(site, password)
        elif choice =="6":
            site = input("What site do you want: ")
            print(f"Password for your {site} is {pm.get_password(site)}")
        elif choice == "q":
            done = True
            print("Good Bye")
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
