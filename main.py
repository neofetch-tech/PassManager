import json
import os
import getpass

PASSWORD_FILE = "passwords.json"

def load_passwords():
    if not os.path.exists(PASSWORD_FILE):
        return {}
    with open(PASSWORD_FILE, "r") as f:
        return json.load(f)

def save_passwords(passwords):
    with open(PASSWORD_FILE, "w") as f:
        json.dump(passwords, f, indent=4)

def add_password(passwords):
    site = input("Enter site name: ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    passwords[site] = {"username": username, "password": password}
    save_passwords(passwords)
    print("Password added.")

def view_passwords(passwords):
    if not passwords:
        print("No passwords stored.")
        return
    for site, creds in passwords.items():
        print(f"Site: {site}")
        print(f"  Username: {creds['username']}")
        print(f"  Password: {creds['password']}")
        print("-" * 20)

def delete_password(passwords):
    site = input("Enter site name to delete: ")
    if site in passwords:
        del passwords[site]
        save_passwords(passwords)
        print("Deleted.")
    else:
        print("Site not found.")

def main():
    passwords = load_passwords()
    while True:
        print("\nPassword Manager")
        print("1. Add password")
        print("2. View passwords")
        print("3. Delete password")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_password(passwords)
        elif choice == "2":
            view_passwords(passwords)
        elif choice == "3":
            delete_password(passwords)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()